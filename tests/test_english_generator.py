import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import web_app
from llm.english_generator import EnglishQuestionGenerator, english_generator


class EnglishGeneratorUnitTests(unittest.TestCase):
    def setUp(self):
        self.generator = EnglishQuestionGenerator()

    def test_cr_generation_schema(self):
        q = self.generator.generate_cr_question(question_type="strengthen", difficulty=4)
        self.assertIsInstance(q, dict)
        self.assertEqual(len(q["options"]), 5, "GMAT question must have exactly 5 options")
        self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])
        self.assertIn("stimulus", q)
        if isinstance(q["stimulus"], dict):
            self.assertTrue(q["stimulus"].get("premise") or q["stimulus"].get("raw"))
        self.assertTrue(q.get("trap_type"))

    def test_rc_generation_schema(self):
        passage = self.generator.generate_rc_passage(category="economics", difficulty=3, question_count=3)
        self.assertIsInstance(passage, dict)
        self.assertGreaterEqual(len(passage.get("paragraphs", [])), 2)
        questions = passage.get("questions", [])
        self.assertGreaterEqual(len(questions), 1)
        for q in questions:
            self.assertEqual(len(q["options"]), 5)
            self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])

    def test_grammar_generation_schema(self):
        g = self.generator.generate_grammar_question(subtopic="modifiers", level=2)
        self.assertIsInstance(g, dict)
        self.assertIn(len(g["options"]), [4, 5])
        self.assertTrue(g.get("grammar_rule"))
        self.assertTrue(g.get("memory_rule"))

    def test_drill_batch_generation(self):
        drill = self.generator.generate_drill_set(mode="cr", count=3, target_difficulty=4)
        self.assertEqual(drill["mode"], "cr")
        self.assertEqual(len(drill["questions"]), 3)

    def test_fallback_when_no_llm(self):
        # Explicitly disable LLM to verify fallback to curated dataset
        self.generator.client = None
        q = self.generator.generate_cr_question(question_type="weaken")
        self.assertIsInstance(q, dict)
        self.assertEqual(len(q["options"]), 5)
        self.assertIn(q["correct_option_index"], [0, 1, 2, 3, 4])


class EnglishGeneratorApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(web_app.app)

    def test_api_generate_cr(self):
        res = self.client.post("/api/english/generate/cr", json={"question_type": "assumption", "difficulty": 3})
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()
        self.assertEqual(len(data["options"]), 5)
        self.assertIn(data["correct_option_index"], [0, 1, 2, 3, 4])

    def test_api_generate_rc(self):
        res = self.client.post("/api/english/generate/rc", json={"category": "technology", "difficulty": 3, "question_count": 2})
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()
        self.assertIn("paragraphs", data)
        self.assertIn("questions", data)

    def test_api_generate_grammar(self):
        res = self.client.post("/api/english/generate/grammar", json={"subtopic": "parallelism", "level": 2})
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()
        self.assertIn(len(data["options"]), [4, 5])

    def test_api_generate_drill(self):
        res = self.client.post("/api/english/generate/drill", json={"mode": "mixed", "count": 4, "target_difficulty": 3})
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()
        self.assertEqual(data["count"], 4)


if __name__ == "__main__":
    unittest.main()
