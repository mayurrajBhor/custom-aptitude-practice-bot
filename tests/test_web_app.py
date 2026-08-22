import os
import json
import unittest
from pathlib import Path

os.environ.setdefault("GROQ_API_KEY", "test-key")

from fastapi.testclient import TestClient

import web_app
from database.db_manager import DatabaseManager


LOCAL_VEDIC_PATTERN_ID = 3001


class WebPracticeSessionTests(unittest.TestCase):
    def setUp(self):
        web_app.SESSIONS.clear()
        self.client = TestClient(web_app.app)

    def start_local_session(self, target_count=3):
        response = self.client.post(
            "/api/session/start",
            json={
                "pattern_ids": [LOCAL_VEDIC_PATTERN_ID],
                "mode": "quick",
                "target_count": target_count,
            },
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        return payload["session_id"], payload

    def test_session_start_prefills_entire_question_set(self):
        session_id, payload = self.start_local_session(target_count=3)
        session = web_app.SESSIONS[session_id]

        self.assertTrue(session["prefilled"])
        self.assertEqual(payload["total_questions"], 3)
        self.assertEqual(len(session["pool"]), 3)
        self.assertIsNone(session["current_question"])

    def test_next_uses_prefilled_questions_without_generating_mid_session(self):
        session_id, _ = self.start_local_session(target_count=2)
        original_fill = web_app._fill_question_pool

        def fail_if_called(*args, **kwargs):
            raise AssertionError("Questions should not be generated after the session starts.")

        web_app._fill_question_pool = fail_if_called
        try:
            first = self.client.post(f"/api/session/{session_id}/next")
            self.assertEqual(first.status_code, 200, first.text)
            self.assertEqual(first.json()["question"]["question_number"], 1)

            current = web_app.SESSIONS[session_id]["current_question"]
            answer = self.client.post(
                f"/api/session/{session_id}/answer",
                json={"answer_index": current["correct_option_index"]},
            )
            self.assertEqual(answer.status_code, 200, answer.text)

            second = self.client.post(f"/api/session/{session_id}/next")
            self.assertEqual(second.status_code, 200, second.text)
            self.assertEqual(second.json()["question"]["question_number"], 2)
        finally:
            web_app._fill_question_pool = original_fill

    def test_stop_practice_keeps_active_question_in_review(self):
        session_id, _ = self.start_local_session(target_count=3)
        question_response = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(question_response.status_code, 200, question_response.text)
        question_text = question_response.json()["question"]["question_text"]

        stop_response = self.client.post(f"/api/session/{session_id}/stop")
        self.assertEqual(stop_response.status_code, 200, stop_response.text)
        summary = stop_response.json()["summary"]
        self.assertTrue(summary["stopped"])
        self.assertEqual(summary["skipped_count"], 1)
        self.assertEqual(summary["total_questions"], 1)
        self.assertEqual(summary["planned_total_questions"], 3)

        review = self.client.get(f"/api/session/{session_id}/review")
        self.assertEqual(review.status_code, 200, review.text)
        questions = review.json()["questions"]
        self.assertEqual(len(questions), 1)
        self.assertTrue(questions[0]["is_skipped"])
        self.assertIsNone(questions[0]["selected_option_index"])
        self.assertEqual(questions[0]["question_text"], question_text)

        next_after_stop = self.client.post(f"/api/session/{session_id}/next")
        self.assertTrue(next_after_stop.json()["complete"])

    def test_answered_session_review_contains_selected_answer(self):
        session_id, _ = self.start_local_session(target_count=1)
        self.client.post(f"/api/session/{session_id}/next")
        current = web_app.SESSIONS[session_id]["current_question"]

        answer = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"answer_index": current["correct_option_index"]},
        )
        self.assertEqual(answer.status_code, 200, answer.text)
        payload = answer.json()
        self.assertTrue(payload["complete"])
        self.assertEqual(payload["summary"]["score"], 1)
        self.assertEqual(payload["summary"]["review_count"], 1)

        review = self.client.get(f"/api/session/{session_id}/review").json()
        self.assertEqual(review["questions"][0]["selected_option_index"], current["correct_option_index"])
        self.assertFalse(review["questions"][0].get("is_skipped", False))

    def test_database_network_error_is_safe_for_browser(self):
        raw_error = (
            'connection to server at "aws-1-ap-southeast-2.pooler.supabase.com", '
            "port 6543 failed: Permission denied Is the server running on that host "
            "and accepting TCP/IP connections?"
        )

        message = web_app._public_exception_message(Exception(raw_error))

        self.assertIn("Database cannot be reached from this environment", message)
        self.assertIn("Using the local practice catalog", message)
        self.assertNotIn("aws-1-ap-southeast-2", message)
        self.assertNotIn("6543", message)

    def test_fast_catalog_returns_without_database_sync(self):
        response = self.client.get("/api/catalog/fast")
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertTrue(payload["fast"])
        self.assertEqual(payload["source"], "local")
        self.assertGreater(len(payload["categories"]), 0)

    def test_explicit_variant_filter_restricts_selected_hybrid_types(self):
        variants = web_app.generator.get_hybrid_variants("Speed Addition and Complements")
        self.assertGreater(len(variants), 1)
        chosen = variants[:2]

        response = self.client.post(
            "/api/session/start",
            json={
                "pattern_ids": [LOCAL_VEDIC_PATTERN_ID],
                "mode": "quick",
                "target_count": 3,
                "variant_selection": {str(LOCAL_VEDIC_PATTERN_ID): chosen},
            },
        )

        self.assertEqual(response.status_code, 200, response.text)
        session = web_app.SESSIONS[response.json()["session_id"]]
        hybrid_types = {item.get("hybrid_type") for item in session["items"] if item.get("hybrid_type")}
        self.assertEqual(hybrid_types, set(chosen))
        self.assertEqual(len(session["items"]), 2)

    def test_explicit_variant_dispatch_does_not_randomize_subtype(self):
        single_digit = web_app.generator._generate_hybrid("vedic_addition::single_digit", difficulty=1)
        two_digit = web_app.generator._generate_hybrid("vedic_addition::two_digit_add_single_digit", difficulty=1)

        self.assertIsNotNone(single_digit)
        self.assertIsNotNone(two_digit)
        self.assertRegex(single_digit["question_text"], r"Add mentally: [3-9] \+ [3-9]")
        self.assertRegex(two_digit["question_text"], r"Add mentally: \d{2} \+ \d")

    def test_adaptive_pattern_order_prefers_weak_patterns(self):
        original_db = web_app.db

        class FakeDb:
            def get_pattern_progress_details(self, user_id, pattern_ids):
                return [
                    {"id": 11, "weakness_score": 12, "total_attempts": 8},
                    {"id": 22, "weakness_score": 80, "total_attempts": 1},
                    {"id": 33, "weakness_score": 40, "total_attempts": 0},
                ]

        web_app.db = FakeDb()
        try:
            ordered = web_app._order_pattern_ids_for_adaptive_practice([11, 22, 33], 123456789, True)
        finally:
            web_app.db = original_db

        self.assertEqual(ordered, [22, 33, 11])

    def test_mistake_retry_builds_exact_saved_questions(self):
        original_db = web_app.db

        class FakeDb:
            def get_mistake_questions(self, user_id, mistake_ids=None, pattern_id=None, limit=20):
                return [
                    {
                        "id": 7,
                        "pattern_id": 42,
                        "pattern_name": "Percent Change",
                        "topic_name": "Percentage",
                        "question_text": "What is 20% of 150?",
                        "options": json.dumps(["20", "25", "30", "35"]),
                        "correct_option_index": 2,
                        "selected_option_index": 1,
                        "explanation": "20% of 150 is 30.",
                        "difficulty": 2,
                        "missed_count": 3,
                    }
                ]

        web_app.db = FakeDb()
        try:
            questions, items, pattern_names = web_app._build_mistake_session_items(123456789, [7], None, 5)
        finally:
            web_app.db = original_db

        self.assertEqual(pattern_names, ["Percent Change"])
        self.assertEqual(items[0]["pattern_id"], 42)
        self.assertEqual(questions[0]["mistake_id"], 7)
        self.assertEqual(questions[0]["question_text"], "What is 20% of 150?")
        self.assertEqual(questions[0]["options"], ["20", "25", "30", "35"])
        self.assertTrue(questions[0]["saved"])


class DatabaseManagerTests(unittest.TestCase):
    def test_execute_query_sets_search_path_before_query(self):
        class FakeCursor:
            description = ("ok",)

            def __init__(self):
                self.executed = []

            def execute(self, query, params=None):
                self.executed.append((query, params))

            def fetchall(self):
                return [{"ok": True}]

        class FakeConnection:
            closed = 0

            def __init__(self):
                self.cursor_instance = FakeCursor()
                self.committed = False

            def poll(self):
                return None

            def cursor(self):
                return self.cursor_instance

            def commit(self):
                self.committed = True

        manager = DatabaseManager()
        manager.conn = FakeConnection()
        result = manager.execute_query("SELECT 1", retries=0)

        executed = manager.conn.cursor_instance.executed
        self.assertEqual(executed[0], ("SET search_path TO aptitude_practice, public", None))
        self.assertEqual(executed[1], ("SELECT 1", None))
        self.assertEqual(result, [{"ok": True}])
        self.assertTrue(manager.conn.committed)

    def test_record_question_attempt_stores_full_question_history(self):
        calls = []
        manager = DatabaseManager()

        def capture(query, params=None):
            calls.append((query, params))
            return True

        manager.execute_query = capture
        manager.record_question_attempt(
            123456789,
            42,
            True,
            3.25,
            session_uuid="session-1",
            question_number=2,
            question_text="What is 20% of 150?",
            options=["20", "25", "30", "35"],
            correct_option_index=2,
            selected_option_index=2,
            explanation="20% of 150 is 30.",
            difficulty=3,
            is_skipped=False,
        )

        query, params = calls[0]
        self.assertIn("question_text", query)
        self.assertIn("selected_option_index", query)
        self.assertEqual(params[2], "session-1")
        self.assertEqual(params[3], 2)
        self.assertEqual(params[4], "What is 20% of 150?")
        self.assertEqual(json.loads(params[6]), ["20", "25", "30", "35"])
        self.assertEqual(params[7], 2)
        self.assertEqual(params[8], 2)
        self.assertEqual(params[11], True)
        self.assertEqual(params[12], False)

    def test_update_user_progress_tracks_wrong_attempts(self):
        calls = []
        manager = DatabaseManager()

        def capture(query, params=None):
            calls.append((query, params))
            if "SELECT * FROM user_progress" in query:
                return []
            if "SELECT difficulty_level FROM patterns" in query:
                return [{"difficulty_level": 2}]
            return True

        manager.execute_query = capture
        manager.update_user_progress(123456789, 42, False, 2, time_taken=18)

        insert_query, insert_params = calls[-1]
        self.assertIn("wrong_attempts", insert_query)
        self.assertEqual(insert_params[4], 1)


class FrontendContractTests(unittest.TestCase):
    def test_stop_button_and_skipped_review_are_wired(self):
        root = Path(__file__).resolve().parents[1]
        index_html = (root / "web" / "index.html").read_text(encoding="utf-8")
        app_js = (root / "web" / "app.js").read_text(encoding="utf-8")
        styles_css = (root / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn('id="stopPracticeButton"', index_html)
        self.assertIn("async function stopPractice()", app_js)
        self.assertIn("/stop", app_js)
        self.assertIn("is_skipped", app_js)
        self.assertIn("Skipped", app_js)
        self.assertIn(".review-card.is-skipped", styles_css)

    def test_adaptive_progress_and_mistake_actions_are_wired(self):
        root = Path(__file__).resolve().parents[1]
        index_html = (root / "web" / "index.html").read_text(encoding="utf-8")
        app_js = (root / "web" / "app.js").read_text(encoding="utf-8")
        styles_css = (root / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("recommended_pattern_ids", app_js)
        self.assertIn("weakness_score", app_js)
        self.assertIn("wrong_attempts", app_js)
        self.assertIn("data-mistake-retry", app_js)
        self.assertIn("data-mistake-similar", app_js)
        self.assertIn("data-mistake-pattern", app_js)
        self.assertIn("retry_mistakes", app_js)
        self.assertIn("startMistakeRetry", app_js)
        self.assertIn("startAllMistakeRetry", app_js)
        self.assertIn("startAdaptivePractice", app_js)
        self.assertIn("smart_plan", app_js)
        self.assertIn("renderSmartPlan", app_js)
        self.assertIn("data-smart-revision-all", app_js)
        self.assertIn("data-mission-key", app_js)
        self.assertIn("questionScore", index_html)
        self.assertIn("questionStreak", index_html)
        self.assertIn("questionCombo", index_html)
        self.assertIn("confettiLayer", index_html)
        self.assertIn("progress-visual-grid", index_html)
        self.assertIn("weeklyHeatmap", index_html)
        self.assertIn("weakRadar", index_html)
        self.assertIn("triggerHaptic", app_js)
        self.assertIn("triggerConfetti", app_js)
        self.assertIn("is-rippling", app_js)
        self.assertIn("const AUTO_ADVANCE_MS = 600", app_js)
        self.assertIn("markAnswerPending", app_js)
        self.assertIn("is-pending", app_js)
        self.assertIn("/api/catalog/fast", app_js)
        self.assertIn("/summary", app_js)
        self.assertIn("/smart-plan", app_js)
        self.assertIn("/progress", app_js)
        self.assertIn("smartCoachCard", index_html)
        self.assertIn(".smart-coach", styles_css)
        self.assertIn(".mission-row", styles_css)
        self.assertIn(".question-hud", styles_css)
        self.assertIn(".progress-visual-card", styles_css)
        self.assertIn("@keyframes control-ripple", styles_css)
        self.assertIn("@keyframes answer-lock", styles_css)
        self.assertIn(".feedback-panel.is-checking", styles_css)
        self.assertIn("@keyframes answer-correct-glow", styles_css)
        self.assertIn(".progress-pattern-card.is-mastered", styles_css)
        self.assertIn(".mistake-answer-grid", styles_css)
        self.assertIn(".mistake-why", styles_css)
        self.assertIn("/static/styles.css?v=28", index_html)
        self.assertIn("/static/app.js?v=27", index_html)

    def test_smart_daily_plan_prioritizes_weak_patterns_and_missions(self):
        plan = web_app._build_smart_daily_plan(
            weak_patterns=[
                {
                    "id": 101,
                    "name": "Percentage Basics",
                    "topic_name": "Percentage",
                    "mastery_score": 0.35,
                    "total_attempts": 6,
                    "accuracy": 50,
                    "avg_time_seconds": 12,
                    "weakness_score": 74,
                    "open_mistakes": 1,
                },
                {
                    "id": 102,
                    "name": "Successive Discounts",
                    "topic_name": "Percentage",
                    "mastery_score": 0.1,
                    "total_attempts": 0,
                    "accuracy": 0,
                    "avg_time_seconds": 0,
                    "weakness_score": 68,
                    "open_mistakes": 0,
                },
            ],
            mistakes=[{"id": 501}],
            today_summary={"total_attempts": 8, "correct_attempts": 5},
            today_pattern_attempts=[
                {"pattern_id": 101, "pattern_name": "Percentage Basics", "attempts": 3, "correct": 2},
            ],
            mistake_retry_count=1,
        )

        self.assertIn("Today revise these 2 weak patterns", plan["coach_line"])
        self.assertEqual([item["id"] for item in plan["revision_queue"]], [101, 102])
        mission_by_key = {mission["key"]: mission for mission in plan["missions"]}
        self.assertEqual(mission_by_key["solve_20"]["progress"], 8)
        self.assertEqual(mission_by_key["improve_weak"]["progress"], 2)
        self.assertEqual(mission_by_key["retry_5_mistakes"]["progress"], 1)
        self.assertFalse(mission_by_key["solve_20"]["completed"])
        self.assertEqual(mission_by_key["retry_5_mistakes"]["reward"]["streak_shields"], 1)


if __name__ == "__main__":
    unittest.main()
