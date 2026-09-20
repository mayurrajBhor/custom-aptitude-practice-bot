import json
import re
import unittest
from fastapi.testclient import TestClient

import web_app


class EnglishFrontendIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(web_app.app)
        cls.html_response = cls.client.get("/")
        cls.html = cls.html_response.text

    def test_index_html_loads_successfully(self):
        self.assertEqual(self.html_response.status_code, 200)

    def test_navigation_tabs_order(self):
        # Verify navigation has Practice, English, and Progress in that order
        self.assertIn('data-screen-target="practice"', self.html)
        self.assertIn('data-screen-target="english"', self.html)
        self.assertIn('data-screen-target="progress"', self.html)

        practice_pos = self.html.find('data-screen-target="practice"')
        english_pos = self.html.find('data-screen-target="english"')
        progress_pos = self.html.find('data-screen-target="progress"')

        self.assertLess(practice_pos, english_pos, "Practice tab must come before English tab")
        self.assertLess(english_pos, progress_pos, "English tab must come before Progress tab")

    def test_english_screen_container_exists(self):
        self.assertIn('id="englishScreen"', self.html, "Must have #englishScreen container in index.html")

    def test_english_static_assets_linked(self):
        self.assertIn('/static/english.css', self.html, "Must link english.css")
        self.assertIn('/static/english_db.js', self.html, "Must include english_db.js")
        self.assertIn('/static/english_data.js', self.html, "Must include english_data.js")
        self.assertIn('/static/english_app.js', self.html, "Must include english_app.js")

    def test_static_assets_served_by_fastapi(self):
        css_res = self.client.get("/static/english.css")
        self.assertEqual(css_res.status_code, 200)
        self.assertIn("--verbal-navy", css_res.text)

        db_res = self.client.get("/static/english_db.js")
        self.assertEqual(db_res.status_code, 200)
        self.assertIn("AptitudeEnglishDB", db_res.text)

        data_res = self.client.get("/static/english_data.js")
        self.assertEqual(data_res.status_code, 200)
        self.assertIn("window.ENGLISH_DATA", data_res.text)

        app_res = self.client.get("/static/english_app.js")
        self.assertEqual(app_res.status_code, 200)
        self.assertIn("window.EnglishApp", app_res.text)
        self.assertIn("QuestionRunner", app_res.text)
        self.assertIn("ReviewUI", app_res.text)
        self.assertIn("FlashcardUI", app_res.text)

    def test_english_data_schema_and_quantities(self):
        data_res = self.client.get("/static/english_data.js")
        self.assertEqual(data_res.status_code, 200)
        text = data_res.text
        json_str = text.split("window.ENGLISH_DATA = ", 1)[1].rstrip(";\r\n ")
        data = json.loads(json_str)

        # 1. Critical Reasoning
        self.assertIn("CR_QUESTIONS", data)
        self.assertGreaterEqual(len(data["CR_QUESTIONS"]), 20)
        for q in data["CR_QUESTIONS"]:
            self.assertEqual(len(q["options"]), 5, f"{q['id']} must have exactly 5 choices")
            self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])
            self.assertTrue(q.get("stimulus"), f"{q['id']} must have a stimulus")
            self.assertTrue(q.get("trap_type"), f"{q['id']} must identify a trap type")
            self.assertEqual(len(q["option_explanations"]), 5, f"{q['id']} must have explanations for all 5 choices")

        # 2. Reading Comprehension
        self.assertIn("RC_PASSAGES", data)
        self.assertGreaterEqual(len(data["RC_PASSAGES"]), 8)
        domains = {p.get("category") for p in data["RC_PASSAGES"]}
        for expected_domain in ["business", "economics", "science", "technology", "history", "social_science", "environment", "arts_and_culture"]:
            self.assertIn(expected_domain, domains, f"Missing domain {expected_domain}")

        for p in data["RC_PASSAGES"]:
            self.assertGreaterEqual(len(p["paragraphs"]), 2, f"Passage {p['id']} must have multiple paragraphs")
            self.assertGreaterEqual(len(p["questions"]), 2, f"Passage {p['id']} must have multiple questions")
            for q in p["questions"]:
                self.assertEqual(len(q["options"]), 5)
                self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])

        # 3. Foundation Grammar
        self.assertIn("GRAMMAR_QUESTIONS", data)
        self.assertGreaterEqual(len(data["GRAMMAR_QUESTIONS"]), 25)
        for g in data["GRAMMAR_QUESTIONS"]:
            self.assertIn(g.get("level"), [1, 2, 3, 4])
            self.assertTrue(g.get("grammar_rule"))
            self.assertTrue(g.get("why_it_works"))
            self.assertTrue(g.get("memory_rule"))

        # 4. Foundation Vocabulary
        self.assertIn("VOCABULARY_ITEMS", data)
        self.assertGreaterEqual(len(data["VOCABULARY_ITEMS"]), 30)
        for v in data["VOCABULARY_ITEMS"]:
            self.assertTrue(v.get("word"))
            self.assertTrue(v.get("definition"))
            self.assertTrue(v.get("synonyms"))
            self.assertTrue(v.get("memory_aid"))

    def test_english_app_subtabs_and_features_present(self):
        app_res = self.client.get("/static/english_app.js")
        self.assertEqual(app_res.status_code, 200)
        text = app_res.text

        # Verify 3 subtabs
        self.assertIn('data-subtab="gmat_verbal"', text)
        self.assertIn('data-subtab="foundation"', text)
        self.assertIn('data-subtab="progress"', text)

        # Verify 45-min simulation and 23 questions
        self.assertIn("45-Min Verbal Simulation", text)
        self.assertIn("45 * 60", text)

        # Verify Variant-Specific Trajectory
        self.assertIn("Variant-Specific Trajectory Chart", text)
        self.assertIn("engVariantSelect", text)

        # Verify Error Log with manual reclassification
        self.assertIn("English Error Log", text)
        self.assertIn("reclassify-error-btn", text)

        # Verify Incomplete Session Resume
        self.assertIn("Continue English Session", text)
        self.assertIn("getActiveEnglishSession", text)

        # Verify Spaced Repetition Flashcards
        self.assertIn("FlashcardUI", text)
        self.assertIn("recordVocabCardReview", text)


if __name__ == "__main__":
    unittest.main()
