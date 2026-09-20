import unittest
import os
from fastapi.testclient import TestClient

os.environ.setdefault("GROQ_API_KEY", "test-key")

import web_app


class EnglishBackendApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(web_app.app)

    def test_english_catalog_endpoint(self):
        response = self.client.get("/api/english/catalog")
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertIn("critical_reasoning", data)
        self.assertIn("reading_comprehension", data)
        self.assertIn("foundation_grammar", data)
        self.assertIn("foundation_vocabulary", data)
        self.assertGreaterEqual(data["critical_reasoning"]["total_questions"], 20)
        self.assertGreaterEqual(data["reading_comprehension"]["total_passages"], 8)
        self.assertGreaterEqual(data["foundation_grammar"]["total_questions"], 25)
        self.assertGreaterEqual(data["foundation_vocabulary"]["total_items"], 30)

    def test_english_questions_endpoint(self):
        response = self.client.get("/api/english/questions")
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertIn("questions", data)
        self.assertGreaterEqual(len(data["questions"]), 20)

        # Validate CR question schema
        cr_questions = [q for q in data["questions"] if q.get("subsection") == "critical_reasoning"]
        self.assertGreaterEqual(len(cr_questions), 1)
        sample_cr = cr_questions[0]
        self.assertEqual(len(sample_cr["options"]), 5, "GMAT question must have exactly 5 options")
        self.assertIn(sample_cr["correct_option_index"], [0, 1, 2, 3, 4])
        self.assertEqual(len(sample_cr["option_explanations"]), 5, "Must have 5 option explanations")
        self.assertTrue(sample_cr.get("stimulus"), "CR must have stimulus")
        self.assertTrue(sample_cr.get("trap_type"), "CR must have trap type")

    def test_verbal_simulation_endpoint(self):
        response = self.client.get("/api/english/simulation/verbal")
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertEqual(data["mode"], "simulation")
        self.assertEqual(data["total_questions"], 23, "Official GMAT Verbal has exactly 23 questions")
        self.assertEqual(data["time_limit_seconds"], 2700, "Official GMAT Verbal is 45 minutes (2700s)")
        self.assertEqual(len(data["questions"]), 23)

        # Check for both CR and RC
        has_cr = any(q.get("subsection") == "critical_reasoning" for q in data["questions"])
        has_rc = any(q.get("subsection") == "reading_comprehension" for q in data["questions"])
        self.assertTrue(has_cr, "Simulation must contain Critical Reasoning")
        self.assertTrue(has_rc, "Simulation must contain Reading Comprehension")

        # Every question must have 5 options
        for i, q in enumerate(data["questions"]):
            self.assertEqual(len(q["options"]), 5, f"Question {i+1} must have exactly 5 options")
            self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])

    def test_verbal_diagnostic_endpoint(self):
        response = self.client.get("/api/english/diagnostic/verbal")
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertEqual(data["mode"], "diagnostic_verbal")
        self.assertEqual(data["total_questions"], 15)
        self.assertEqual(len(data["questions"]), 15)

    def test_foundation_diagnostic_endpoint(self):
        response = self.client.get("/api/english/diagnostic/foundation")
        self.assertEqual(response.status_code, 200, response.text)
        data = response.json()
        self.assertEqual(data["mode"], "diagnostic_foundation")
        self.assertEqual(data["total_questions"], 16)
        self.assertEqual(len(data["questions"]), 16)

    def test_filter_by_subsection(self):
        response_cr = self.client.get("/api/english/questions?subsection=critical_reasoning")
        self.assertEqual(response_cr.status_code, 200)
        data_cr = response_cr.json()
        self.assertTrue(all(q.get("subsection") == "critical_reasoning" for q in data_cr["questions"]))

        response_rc = self.client.get("/api/english/questions?subsection=reading_comprehension")
        self.assertEqual(response_rc.status_code, 200)
        data_rc = response_rc.json()
        self.assertTrue(all(q.get("subsection") == "reading_comprehension" for q in data_rc["questions"]))


if __name__ == "__main__":
    unittest.main()

