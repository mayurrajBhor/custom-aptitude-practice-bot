import unittest
from fastapi.testclient import TestClient

import web_app
from local_catalog import get_local_catalog_payload, get_local_pattern, is_local_pattern_id
from llm.gmat import (
    ALL_GMAT_PATTERNS_METADATA,
    DAY1_LIST,
    DAY2_LIST,
    DAY3_LIST,
    DAY4_LIST,
    get_gmat_generator,
    is_gmat_pattern_id,
)
from llm.generator import generator


class GMATIntegrationTests(unittest.TestCase):
    def setUp(self):
        web_app.SESSIONS.clear()
        self.client = TestClient(web_app.app)

    def test_catalog_contains_all_four_days(self):
        catalog = get_local_catalog_payload()
        quant = next((c for c in catalog if c["name"] == "Quant"), None)
        self.assertIsNotNone(quant, "Quant category missing from local catalog")

        topic_names = [t["name"] for t in quant["topics"]]
        expected_days = [
            "Day 1: Number Sense & Basic Arithmetic",
            "Day 2: Fractions & Decimals",
            "Day 3: Percentages & Commercial Math",
            "Day 4: Ratios, Proportion & Averages",
        ]
        for day in expected_days:
            self.assertIn(day, topic_names)

        day1_topic = next(t for t in quant["topics"] if t["name"] == "Day 1: Number Sense & Basic Arithmetic")
        self.assertEqual(len(day1_topic["patterns"]), 9)

        day2_topic = next(t for t in quant["topics"] if t["name"] == "Day 2: Fractions & Decimals")
        self.assertEqual(len(day2_topic["patterns"]), 15)

        day3_topic = next(t for t in quant["topics"] if t["name"] == "Day 3: Percentages & Commercial Math")
        self.assertEqual(len(day3_topic["patterns"]), 15)

        day4_topic = next(t for t in quant["topics"] if t["name"] == "Day 4: Ratios, Proportion & Averages")
        self.assertEqual(len(day4_topic["patterns"]), 16)

        total_patterns = sum(len(t["patterns"]) for t in quant["topics"] if t["name"].startswith("Day "))
        self.assertEqual(total_patterns, 55)

    def test_all_55_pattern_ids_registered_and_retrievable(self):
        self.assertEqual(len(ALL_GMAT_PATTERNS_METADATA), 55)
        for meta in ALL_GMAT_PATTERNS_METADATA:
            pid = meta["id"]
            self.assertTrue(is_local_pattern_id(pid), f"Pattern {pid} not found in local catalog")
            self.assertTrue(is_gmat_pattern_id(pid))
            pat = get_local_pattern(pid)
            self.assertIsNotNone(pat)
            self.assertGreater(pat["variant_count"], 0)
            self.assertIsNotNone(get_gmat_generator(pid))

    def test_fast_catalog_endpoint_exposes_all_days(self):
        res = self.client.get("/api/catalog/fast")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        quant = next((c for c in data["categories"] if c["name"] == "Quant"), None)
        self.assertIsNotNone(quant)

        topics_map = {t["name"]: t for t in quant["topics"]}
        self.assertIn("Day 1: Number Sense & Basic Arithmetic", topics_map)
        self.assertIn("Day 2: Fractions & Decimals", topics_map)
        self.assertIn("Day 3: Percentages & Commercial Math", topics_map)
        self.assertIn("Day 4: Ratios, Proportion & Averages", topics_map)

    def test_practice_session_start_and_answer_with_mistake_tagging(self):
        # Start a session for Pattern 5031 (Profit and Loss) in Day 3
        res = self.client.post(
            "/api/session/start",
            json={
                "pattern_ids": [5031],
                "time_limit_seconds": 60,
                "mode": "quick",
                "target_count": 2,
            },
        )
        self.assertEqual(res.status_code, 200, res.text)
        session_data = res.json()
        session_id = session_data["session_id"]
        self.assertEqual(session_data["total_questions"], 2)

        # Fetch next question
        q_res = self.client.post(f"/api/session/{session_id}/next")
        self.assertEqual(q_res.status_code, 200)
        q_data = q_res.json()["question"]
        options = q_data["options"]
        self.assertEqual(len(options), 4)

        # Deliberately submit a wrong answer
        session = web_app.SESSIONS[session_id]
        active_q = session["current_question"]
        correct_idx = active_q["correct_option_index"]
        wrong_idx = (correct_idx + 1) % 4

        ans_res = self.client.post(
            f"/api/session/{session_id}/answer",
            json={"answer_index": wrong_idx},
        )
        self.assertEqual(ans_res.status_code, 200)
        ans_data = ans_res.json()
        self.assertFalse(ans_data["is_correct"])
        self.assertIsNotNone(ans_data.get("mistake_classification"))
        self.assertIn("category", ans_data["mistake_classification"])
        self.assertIn("label", ans_data["mistake_classification"])
        self.assertIn("remedy", ans_data["mistake_classification"])

    def test_untimed_accuracy_mode_session(self):
        # Test time_limit_seconds = 0 (Accuracy Mode / untimed)
        res = self.client.post(
            "/api/session/start",
            json={
                "pattern_ids": [5001],
                "time_limit_seconds": 0,
                "mode": "quick",
                "target_count": 1,
            },
        )
        self.assertEqual(res.status_code, 200, res.text)
        session_data = res.json()
        self.assertEqual(session_data["time_limit_seconds"], 0)


if __name__ == "__main__":
    unittest.main()
