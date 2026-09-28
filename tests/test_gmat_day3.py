import unittest
import os
import sys
import random

from llm.gmat.day3_percentages import (
    DAY3_GENERATORS,
    DAY3_PATTERNS_METADATA,
    percentage_fundamentals,
    percentage_increase,
    percentage_decrease,
    new_value_percentage_change,
    reverse_percentage,
    successive_percentage_changes,
    profit_and_loss,
    profit_loss_multipliers,
    markup,
    discount,
    markup_discount_combined,
    successive_discounts,
    percentage_vs_percentage_points,
    more_than_vs_less_than,
    percentage_word_problems,
)
from llm.gmat.mistakes import MISTAKE_CATEGORIES


class TestGmatDay3Percentages(unittest.TestCase):
    def setUp(self):
        self.pattern_ids = list(range(5025, 5040))
        self.all_generators = [
            percentage_fundamentals,
            percentage_increase,
            percentage_decrease,
            new_value_percentage_change,
            reverse_percentage,
            successive_percentage_changes,
            profit_and_loss,
            profit_loss_multipliers,
            markup,
            discount,
            markup_discount_combined,
            successive_discounts,
            percentage_vs_percentage_points,
            more_than_vs_less_than,
            percentage_word_problems,
        ]

    def test_metadata_registry(self):
        """Verify DAY3_PATTERNS_METADATA and DAY3_GENERATORS contain all 15 patterns."""
        self.assertEqual(len(DAY3_PATTERNS_METADATA), 15)
        for pid in self.pattern_ids:
            self.assertIn(pid, DAY3_PATTERNS_METADATA)
            meta = DAY3_PATTERNS_METADATA[pid]
            self.assertEqual(meta["id"], pid)
            self.assertTrue(isinstance(meta["name"], str) and len(meta["name"]) > 0)
            self.assertTrue(isinstance(meta["description"], str) and len(meta["description"]) > 0)
            self.assertTrue(isinstance(meta["variants"], list) and len(meta["variants"]) >= 3)

            # Test DAY3_GENERATORS lookup by int and string
            self.assertIn(pid, DAY3_GENERATORS)
            self.assertIn(str(pid), DAY3_GENERATORS)
            self.assertIn(meta["name"], DAY3_GENERATORS)
            self.assertTrue(callable(DAY3_GENERATORS[pid]))

    def _validate_mcq_structure(self, mcq, expected_difficulty=None, expected_variant=None):
        self.assertIsInstance(mcq, dict)
        self.assertIn("question_text", mcq)
        self.assertIsInstance(mcq["question_text"], str)
        self.assertGreater(len(mcq["question_text"].strip()), 0)

        self.assertIn("options", mcq)
        self.assertIsInstance(mcq["options"], list)
        self.assertEqual(len(mcq["options"]), 4, f"Options length is {len(mcq['options'])}, expected 4")

        # 4 distinct options
        self.assertEqual(len(set(mcq["options"])), 4, f"Options must be distinct: {mcq['options']}")

        self.assertIn("correct_option_index", mcq)
        self.assertIn(mcq["correct_option_index"], [0, 1, 2, 3])
        correct_opt = mcq["options"][mcq["correct_option_index"]]
        self.assertTrue(len(correct_opt.strip()) > 0)

        self.assertIn("explanation", mcq)
        self.assertIsInstance(mcq["explanation"], str)
        self.assertGreater(len(mcq["explanation"].strip()), 0)

        if expected_difficulty is not None:
            self.assertEqual(mcq["difficulty"], max(1, min(5, expected_difficulty)))

        if expected_variant is not None:
            self.assertEqual(mcq["subvariant"], expected_variant)

        # Validate trap_map categories
        self.assertIn("trap_map", mcq)
        self.assertIsInstance(mcq["trap_map"], dict)
        for opt_text, category in mcq["trap_map"].items():
            self.assertIn(
                category,
                MISTAKE_CATEGORIES,
                f"Trap category '{category}' for option '{opt_text}' must exist in MISTAKE_CATEGORIES",
            )

    def test_all_generators_at_multiple_difficulties(self):
        """Test each of the 15 generators across difficulties 1, 3, and 5."""
        for gen in self.all_generators:
            for diff in [1, 3, 5]:
                for _ in range(3):  # multiple runs to verify randomized branches
                    mcq = gen(difficulty=diff)
                    self._validate_mcq_structure(mcq, expected_difficulty=diff)

    def test_all_variants_can_be_forced(self):
        """Test that each pattern's variants can be explicitly forced and match metadata."""
        for pid in self.pattern_ids:
            meta = DAY3_PATTERNS_METADATA[pid]
            gen = DAY3_GENERATORS[pid]
            variants = meta["variants"]
            for var in variants:
                for diff in [1, 2, 4]:
                    mcq = gen(difficulty=diff, forced_variant=var)
                    self._validate_mcq_structure(mcq, expected_difficulty=diff, expected_variant=var)

    def test_boundary_and_invalid_difficulties(self):
        """Verify clamp_level behavior for out-of-range difficulties."""
        for gen in self.all_generators:
            mcq_low = gen(difficulty=-2)
            self._validate_mcq_structure(mcq_low, expected_difficulty=1)

            mcq_high = gen(difficulty=99)
            self._validate_mcq_structure(mcq_high, expected_difficulty=5)

    def test_stress_all_patterns(self):
        """Stress test: 20 random generations per generator to ensure stability and uniqueness."""
        for gen in self.all_generators:
            for _ in range(20):
                diff = random.randint(1, 5)
                mcq = gen(difficulty=diff)
                self._validate_mcq_structure(mcq, expected_difficulty=diff)


if __name__ == "__main__":
    unittest.main()
