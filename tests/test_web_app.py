import os
import json
import time
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

    def test_answer_question_with_typed_answer(self):
        session_id, _ = self.start_local_session(target_count=2)
        self.client.post(f"/api/session/{session_id}/next")
        current = web_app.SESSIONS[session_id]["current_question"]
        correct_val = current["options"][current["correct_option_index"]]

        # Correct typed answer
        res = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"typed_answer": str(correct_val)},
        )
        self.assertEqual(res.status_code, 200, res.text)
        payload = res.json()
        self.assertTrue(payload["is_correct"])
        self.assertEqual(payload["score"], 1)
        self.assertEqual(payload["typed_answer"], str(correct_val))

        # Next question
        self.client.post(f"/api/session/{session_id}/next")
        # Incorrect typed answer
        res_wrong = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"typed_answer": "99999999"},
        )
        self.assertEqual(res_wrong.status_code, 200, res_wrong.text)
        payload_wrong = res_wrong.json()
        self.assertFalse(payload_wrong["is_correct"])
        self.assertEqual(payload_wrong["score"], 1)
        self.assertTrue(payload_wrong["complete"])

        # Check review
        review = self.client.get(f"/api/session/{session_id}/review")
        self.assertEqual(review.status_code, 200)
        history = review.json()["questions"]
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["typed_answer"], str(correct_val))
        self.assertTrue(history[0]["is_correct"])
        self.assertEqual(history[1]["typed_answer"], "99999999")
        self.assertFalse(history[1]["is_correct"])

    def test_timeout_answer_marks_failed_after_30_seconds(self):
        session_id, _ = self.start_local_session(target_count=2)
        q1_res = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(q1_res.status_code, 200, q1_res.text)
        q1 = q1_res.json()["question"]
        self.assertIn("correct_option_index", q1)

        # Submit answer with timeout
        timeout_res = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"is_timeout": True},
        )
        self.assertEqual(timeout_res.status_code, 200, timeout_res.text)
        payload = timeout_res.json()
        self.assertFalse(payload["is_correct"])
        self.assertEqual(payload["time_taken"], 30.0)
        self.assertIsNone(payload["selected_option_index"])
        self.assertEqual(payload["score"], 0)
        self.assertEqual(payload["answered"], 1)
        self.assertFalse(payload["complete"])

        # Moves forward to next question
        q2_res = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(q2_res.status_code, 200, q2_res.text)
        q2 = q2_res.json()["question"]
        self.assertEqual(q2["question_number"], 2)

        # Verify session review records timeout attempt accurately
        review = self.client.get(f"/api/session/{session_id}/review")
        self.assertEqual(review.status_code, 200)
        history = review.json()["questions"]
        self.assertEqual(len(history), 1)
        self.assertFalse(history[0]["is_correct"])
        self.assertEqual(history[0]["time_taken"], 30.0)
        self.assertIsNone(history[0]["selected_option_index"])

    def test_re_practice_weak_questions_creates_new_session_with_slow_questions(self):
        session_id, _ = self.start_local_session(target_count=2)

        # Question 1: next question
        q1_res = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(q1_res.status_code, 200, q1_res.text)
        q1 = q1_res.json()["question"]

        # Question 1 takes 2.0s and is correct
        web_app.SESSIONS[session_id]["current_started_at"] = time.monotonic() - 2.0
        ans1_res = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"answer_index": q1["correct_option_index"]},
        )
        self.assertEqual(ans1_res.status_code, 200, ans1_res.text)
        self.assertTrue(ans1_res.json()["is_correct"])

        # Question 2: next question
        q2_res = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(q2_res.status_code, 200, q2_res.text)
        q2 = q2_res.json()["question"]

        # Question 2 takes 15.0s (or is timeout 30.0s)
        ans2_res = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"is_timeout": True},
        )
        self.assertEqual(ans2_res.status_code, 200, ans2_res.text)
        ans2_payload = ans2_res.json()
        self.assertTrue(ans2_payload["complete"])

        # Verifies session summary has avg_time > 0, weak_count >= 1
        summary = ans2_payload["summary"]
        self.assertGreater(summary["avg_time"], 0)
        self.assertGreaterEqual(summary["weak_count"], 1)

        # Calls POST /api/session/{session_id}/re-practice-weak
        re_res = self.client.post(f"/api/session/{session_id}/re-practice-weak")
        self.assertEqual(re_res.status_code, 200, re_res.text)
        re_payload = re_res.json()

        # Verifies 200 OK, returns new session with total_questions == 1 (the slow/weak question)
        # Verifies 200 OK, returns new session with total_questions == 2 (matching practice set size, repeating the weak question)
        self.assertIn("session", re_payload)
        new_session = re_payload["session"]
        new_session_id = new_session["session_id"]
        self.assertEqual(new_session["total_questions"], 2)
        self.assertEqual(re_payload["weak_count"], 1)
        self.assertEqual(re_payload["total_questions"], 2)

        # Calls POST /api/session/{new_session_id}/next and verifies Question 1 of the new session is the slow question
        new_q1_res = self.client.post(f"/api/session/{new_session_id}/next")
        self.assertEqual(new_q1_res.status_code, 200, new_q1_res.text)
        new_q1 = new_q1_res.json()["question"]
        self.assertEqual(new_q1["question_number"], 1)
        self.assertEqual(new_q1["question_text"], q2["question_text"])

        # Answer Question 1
        ans_new1 = self.client.post(
            f"/api/session/{new_session_id}/answer",
            json={"answer_index": new_q1["correct_option_index"]},
        )
        self.assertEqual(ans_new1.status_code, 200)
        self.assertFalse(ans_new1.json()["complete"])

        # Question 2 is the repeated weak question filling the full practice set
        new_q2_res = self.client.post(f"/api/session/{new_session_id}/next")
        self.assertEqual(new_q2_res.status_code, 200, new_q2_res.text)
        new_q2 = new_q2_res.json()["question"]
        self.assertEqual(new_q2["question_number"], 2)
        self.assertEqual(new_q2["question_text"], q2["question_text"])

        # Answer Question 2 to complete the full 2-question drill set
        ans_new2 = self.client.post(
            f"/api/session/{new_session_id}/answer",
            json={"answer_index": new_q2["correct_option_index"]},
        )
        self.assertEqual(ans_new2.status_code, 200)
        self.assertTrue(ans_new2.json()["complete"])

    def test_re_practice_weak_questions_repeats_to_match_full_set_count(self):
        # 5-question practice session with 2 weak questions
        session_id, _ = self.start_local_session(target_count=5)
        questions = []
        for i in range(5):
            q_res = self.client.post(f"/api/session/{session_id}/next")
            self.assertEqual(q_res.status_code, 200)
            q = q_res.json()["question"]
            questions.append(q)
            # Questions 1 and 3 are slow/weak, others are fast
            if i in (1, 3):
                web_app.SESSIONS[session_id]["current_started_at"] = time.monotonic() - 25.0
                ans_res = self.client.post(f"/api/session/{session_id}/answer", json={"is_timeout": True})
            else:
                web_app.SESSIONS[session_id]["current_started_at"] = time.monotonic() - 2.0
                ans_res = self.client.post(
                    f"/api/session/{session_id}/answer",
                    json={"answer_index": q["correct_option_index"]},
                )
            self.assertEqual(ans_res.status_code, 200)

        # Call re-practice weak
        re_res = self.client.post(f"/api/session/{session_id}/re-practice-weak")
        self.assertEqual(re_res.status_code, 200)
        payload = re_res.json()
        new_session = payload["session"]
        new_session_id = new_session["session_id"]

        # Weak count is 2, but total_questions is 5 (full set size)
        self.assertEqual(payload["weak_count"], 2)
        self.assertEqual(payload["total_questions"], 5)
        self.assertEqual(new_session["total_questions"], 5)

        # The 5 questions should cycle the 2 weak questions repeatedly
        weak_texts = {questions[1]["question_text"], questions[3]["question_text"]}
        seen_texts = []
        for q_num in range(1, 6):
            nq_res = self.client.post(f"/api/session/{new_session_id}/next")
            self.assertEqual(nq_res.status_code, 200)
            nq = nq_res.json()["question"]
            self.assertEqual(nq["question_number"], q_num)
            self.assertIn(nq["question_text"], weak_texts)
            seen_texts.append(nq["question_text"])
            self.client.post(
                f"/api/session/{new_session_id}/answer",
                json={"answer_index": nq["correct_option_index"]},
            )

        # Confirm all 5 questions were from the weak questions set and repeated
        self.assertEqual(len(seen_texts), 5)
        self.assertGreater(seen_texts.count(questions[1]["question_text"]), 1)
        self.assertGreater(seen_texts.count(questions[3]["question_text"]), 1)

    def test_re_practice_weak_fallback_and_empty_validation(self):
        # Empty session (no questions answered yet) should 404
        # Empty session (no questions answered yet) should gracefully succeed with fallback questions matching target_count
        session_id, _ = self.start_local_session(target_count=2)
        res_empty = self.client.post(f"/api/session/{session_id}/re-practice-weak")
        self.assertEqual(res_empty.status_code, 404)
        self.assertIn("No answered questions", res_empty.json()["detail"])

        # Answer 1 question correctly and quickly (fallback kicks in when none are slow/wrong)
        q1_res = self.client.post(f"/api/session/{session_id}/next")
        q1 = q1_res.json()["question"]
        web_app.SESSIONS[session_id]["current_started_at"] = time.monotonic() - 1.0
        self.client.post(
            f"/api/session/{session_id}/answer",
            json={"answer_index": q1["correct_option_index"]},
        )

        res_fallback = self.client.post(f"/api/session/{session_id}/re-practice-weak")
        self.assertEqual(res_fallback.status_code, 200)
        self.assertEqual(res_fallback.json()["session"]["total_questions"], 2)

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
        self.assertIn("applyRecommendationsPayload", app_js)
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
        self.assertIn("/recommendations", app_js)
        self.assertIn("/progress", app_js)
        self.assertNotIn("Today Coach", index_html)
        self.assertNotIn("smartCoachCard", index_html)
        self.assertIn(".question-hud", styles_css)
        self.assertIn(".progress-visual-card", styles_css)
        self.assertIn("@keyframes control-ripple", styles_css)
        self.assertIn("@keyframes answer-lock", styles_css)
        self.assertIn(".feedback-panel.is-checking", styles_css)
        self.assertIn("@keyframes answer-correct-glow", styles_css)
        self.assertIn(".progress-pattern-card.is-mastered", styles_css)
        self.assertIn(".mistake-answer-grid", styles_css)
        self.assertIn("/static/styles.css", index_html)
        self.assertIn("/static/app.js", index_html)
        self.assertIn("topAnswerModeToggle", index_html)
        self.assertIn("numpadPanel", index_html)
        self.assertIn("numpadDisplay", index_html)
        self.assertIn("setAnswerMode", app_js)
        self.assertIn("submitTypedAnswer", app_js)
        self.assertIn("checkAutoSubmit", app_js)
        self.assertIn("autoSubmitTimer", app_js)
        self.assertIn("numpadAutoStatus", index_html)
        self.assertIn(".numpad-grid", styles_css)
        self.assertIn(".answer-mode-toggle", styles_css)
        self.assertIn(".numpad-auto-status", styles_css)
        self.assertIn("QUESTION_TIME_LIMIT_SECONDS = 30", app_js)
        self.assertIn("handleQuestionTimeout", app_js)
        self.assertIn("isAnswerCorrect", app_js)
        self.assertIn("checkDigitInput", app_js)
        self.assertIn("#questionTimer.is-warning", styles_css)
        self.assertIn("#questionTimer.is-urgent", styles_css)
        self.assertIn("resultSpeedStrip", index_html)
        self.assertIn("resultAvgTime", index_html)
        self.assertIn("resultWeakCount", index_html)
        self.assertIn("rePracticeWeakButton", index_html)
        self.assertIn("reviewRePracticeWeakButton", index_html)
        self.assertIn("rePracticeWeakQuestions", app_js)
        self.assertIn("/re-practice-weak", app_js)
        self.assertIn(".result-speed-strip", styles_css)
        self.assertIn(".weak-repractice-banner", styles_css)
        self.assertIn(".time-badge.is-slow", styles_css)

    def test_local_database_and_analytics_contract(self):
        root = Path(__file__).resolve().parents[1]
        local_db_path = root / "web" / "local_db.js"
        self.assertTrue(local_db_path.exists())

        local_db_js = local_db_path.read_text(encoding="utf-8")
        index_html = (root / "web" / "index.html").read_text(encoding="utf-8")
        app_js = (root / "web" / "app.js").read_text(encoding="utf-8")
        styles_css = (root / "web" / "styles.css").read_text(encoding="utf-8")

        for fn in [
            "initLocalDB",
            "recordLocalAttempt",
            "recordLocalSession",
            "getLocalAnalytics",
            "exportLocalDataJSON",
            "exportLocalDataCSV",
            "importLocalDataJSON",
        ]:
            self.assertIn(fn, local_db_js)

        self.assertIn("/static/local_db.js", index_html)
        self.assertIn('id="localAnalyticsCard"', index_html)
        self.assertIn('id="downloadJsonBtn"', index_html)
        self.assertIn('id="downloadCsvBtn"', index_html)
        self.assertIn('id="localJournalContent"', index_html)

        self.assertIn("AptitudeLocalDB", app_js)
        self.assertIn("exportLocalDataJSON", app_js)
        self.assertIn("exportLocalDataCSV", app_js)

        self.assertIn(".local-analytics-card", styles_css)
        self.assertIn(".journal-tabs", styles_css)
        self.assertIn(".journal-attempt-card", styles_css)

    def test_advanced_progress_dashboard_contract(self):
        root = Path(__file__).resolve().parents[1]
        local_db_js = (root / "web" / "local_db.js").read_text(encoding="utf-8")
        index_html = (root / "web" / "index.html").read_text(encoding="utf-8")
        app_js = (root / "web" / "app.js").read_text(encoding="utf-8")
        styles_css = (root / "web" / "styles.css").read_text(encoding="utf-8")

        self.assertIn("getAdvancedLocalAnalytics", local_db_js)

        # Index.html advanced cockpit elements
        for element_id in [
            'id="readinessCockpitCard"',
            'id="readinessScore"',
            'id="readinessTier"',
            'id="readinessPillars"',
            'id="aiPrescriptionsCard"',
            'id="aiPrescriptionsContainer"',
            'id="speedAccuracyMatrixCard"',
            'id="quadMastersList"',
            'id="quadTrapsList"',
            'id="quadRushersList"',
            'id="quadBottlenecksList"',
            'id="pacingStaminaCard"',
            'id="pacingStackedBar"',
            'id="performanceTrendSvg"',
            'id="rootCauseMistakeCard"',
            'id="drillAllMistakesBtn"',
            'id="rootCauseMistakeList"',
        ]:
            self.assertIn(element_id, index_html)

        # App.js handlers
        self.assertIn("renderAdvancedProgressDashboard", app_js)
        self.assertIn("renderPerformanceTrendSvg", app_js)
        self.assertIn("renderRootCauseMistakes", app_js)
        self.assertIn("data-drill-pattern", app_js)

        # Styles.css layout classes
        for css_class in [
            ".readiness-cockpit-card",
            ".readiness-gauge",
            ".ai-prescriptions-card",
            ".quadrant-matrix-grid",
            ".pacing-stacked-bar",
            ".root-cause-mistake-card",
            ".badge-calc",
            ".badge-concept",
        ]:
            self.assertIn(css_class, styles_css)


if __name__ == "__main__":
    unittest.main()
