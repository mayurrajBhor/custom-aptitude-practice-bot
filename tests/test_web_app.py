import os
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


if __name__ == "__main__":
    unittest.main()
