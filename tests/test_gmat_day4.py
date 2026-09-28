"""Comprehensive unit tests for Day 4 GMAT Practice Engine: Ratios, Proportions, and Averages.

Tests Patterns 5040 through 5055 across all variants, multiple difficulty levels,
registry lookups, metadata completeness, and MCQ structural constraints.
"""

import unittest
from typing import Any, Dict, List

from llm.gmat.mistakes import MISTAKE_CATEGORIES
from llm.gmat.day4_ratios_averages import (
    DAY4_GENERATORS,
    DAY4_PATTERNS_METADATA,
    generate_adding_number_to_average,
    generate_average_basics,
    generate_average_change_shortcut,
    generate_direct_proportion,
    generate_gmat_mixed_questions,
    generate_inverse_proportion,
    generate_missing_number_average,
    generate_proportion,
    generate_ratio_basics,
    generate_ratio_changes,
    generate_ratio_one_value_known,
    generate_ratio_variables_x_method,
    generate_ratio_with_total,
    generate_removing_number_from_average,
    generate_weighted_average,
    generate_weighted_average_intuition,
)


class TestGmatDay4Generators(unittest.TestCase):
    """Test suite verifying all Day 4 patterns, variants, and difficulty scaling."""

    PATTERN_FUNCTIONS = [
        ("ratio_basics", 5040, generate_ratio_basics),
        ("ratio_with_total", 5041, generate_ratio_with_total),
        ("ratio_one_value_known", 5042, generate_ratio_one_value_known),
        ("ratio_changes", 5043, generate_ratio_changes),
        ("ratio_variables_x_method", 5044, generate_ratio_variables_x_method),
        ("proportion", 5045, generate_proportion),
        ("direct_proportion", 5046, generate_direct_proportion),
        ("inverse_proportion", 5047, generate_inverse_proportion),
        ("average_basics", 5048, generate_average_basics),
        ("missing_number_average", 5049, generate_missing_number_average),
        ("adding_number_to_average", 5050, generate_adding_number_to_average),
        ("removing_number_from_average", 5051, generate_removing_number_from_average),
        ("average_change_shortcut", 5052, generate_average_change_shortcut),
        ("weighted_average", 5053, generate_weighted_average),
        ("weighted_average_intuition", 5054, generate_weighted_average_intuition),
        ("gmat_mixed_questions", 5055, generate_gmat_mixed_questions),
    ]

    def _assert_valid_mcq(self, mcq: Dict[str, Any], expected_level: int, expected_variant: str = None) -> None:
        """Helper to assert that a generated MCQ strictly obeys schema and content rules."""
        # 1. Question text
        self.assertIn("question_text", mcq)
        self.assertIsInstance(mcq["question_text"], str)
        self.assertTrue(len(mcq["question_text"].strip()) > 10, "Question text too short or empty")

        # 2. Options: exactly 4 distinct non-empty strings
        self.assertIn("options", mcq)
        self.assertIsInstance(mcq["options"], list)
        self.assertEqual(len(mcq["options"]), 4, "MCQ must contain exactly 4 options")
        self.assertEqual(len(set(mcq["options"])), 4, f"Options must all be distinct: {mcq['options']}")
        for opt in mcq["options"]:
            self.assertTrue(len(str(opt).strip()) > 0, "Option text cannot be empty")

        # 3. Correct option index
        self.assertIn("correct_option_index", mcq)
        self.assertIsInstance(mcq["correct_option_index"], int)
        self.assertIn(mcq["correct_option_index"], [0, 1, 2, 3])

        # 4. Explanation
        self.assertIn("explanation", mcq)
        self.assertIsInstance(mcq["explanation"], str)
        self.assertTrue(len(mcq["explanation"].strip()) > 10, "Explanation too short or empty")

        # 5. Difficulty
        self.assertIn("difficulty", mcq)
        self.assertEqual(mcq["difficulty"], max(1, min(5, expected_level)))

        # 6. Trap map
        self.assertIn("trap_map", mcq)
        self.assertIsInstance(mcq["trap_map"], dict)
        for trap_opt, trap_cat in mcq["trap_map"].items():
            self.assertIn(
                trap_cat,
                MISTAKE_CATEGORIES,
                f"Unknown mistake category '{trap_cat}' for option '{trap_opt}' in {mcq.get('pattern_name')}",
            )

        # 7. Subvariant
        if expected_variant:
            self.assertEqual(mcq.get("subvariant"), expected_variant)

    def test_registry_lookups(self):
        """Verify DAY4_GENERATORS supports integer IDs, string IDs, and pattern names."""
        for name, pid, func in self.PATTERN_FUNCTIONS:
            self.assertIn(name, DAY4_GENERATORS, f"Missing name key in DAY4_GENERATORS: {name}")
            self.assertEqual(DAY4_GENERATORS[name], func)

            self.assertIn(pid, DAY4_GENERATORS, f"Missing int ID in DAY4_GENERATORS: {pid}")
            self.assertEqual(DAY4_GENERATORS[pid], func)

            self.assertIn(str(pid), DAY4_GENERATORS, f"Missing str ID in DAY4_GENERATORS: {pid}")
            self.assertEqual(DAY4_GENERATORS[str(pid)], func)

    def test_metadata_completeness(self):
        """Verify DAY4_PATTERNS_METADATA covers all 16 patterns with required fields."""
        for name, pid, _ in self.PATTERN_FUNCTIONS:
            self.assertIn(pid, DAY4_PATTERNS_METADATA, f"Missing metadata for pattern {pid}")
            meta = DAY4_PATTERNS_METADATA[pid]
            self.assertEqual(meta["id"], pid)
            self.assertEqual(meta["name"], name)
            self.assertTrue(len(meta["description"].strip()) > 0)
            self.assertIn("variants", meta)
            self.assertIn("variant_names", meta)
            self.assertEqual(len(meta["variants"]), 5, f"Pattern {pid} should have exactly 5 variants")
            self.assertEqual(meta["variants"], meta["variant_names"])

    def test_generators_at_multiple_difficulties(self):
        """Test each of the 16 generators at difficulties 1, 3, and 5."""
        for name, pid, func in self.PATTERN_FUNCTIONS:
            for diff in [1, 3, 5]:
                mcq = func(difficulty=diff)
                self._assert_valid_mcq(mcq, expected_level=diff)
                self.assertEqual(mcq.get("pattern_name"), name)

    def test_all_variants_can_be_forced(self):
        """Test that every variant across all 16 patterns can be explicitly forced."""
        total_variants_tested = 0
        for name, pid, func in self.PATTERN_FUNCTIONS:
            variants = DAY4_PATTERNS_METADATA[pid]["variants"]
            for variant in variants:
                mcq = func(difficulty=3, forced_variant=variant)
                self._assert_valid_mcq(mcq, expected_level=3, expected_variant=variant)
                total_variants_tested += 1
        self.assertEqual(total_variants_tested, 16 * 5, "Expected 80 distinct variants tested")

    def test_difficulty_clamping_boundary(self):
        """Verify difficulty clamping for out-of-range inputs (<1 and >5)."""
        for _, _, func in self.PATTERN_FUNCTIONS:
            # Below min
            mcq_low = func(difficulty=-1)
            self.assertEqual(mcq_low["difficulty"], 1)

            # Above max
            mcq_high = func(difficulty=10)
            self.assertEqual(mcq_high["difficulty"], 5)

    def test_repeated_generation_randomness(self):
        """Verify questions generated repeatedly produce valid non-colliding options."""
        for _, _, func in self.PATTERN_FUNCTIONS:
            for _ in range(5):
                test_diff = 2
                mcq = func(difficulty=test_diff)
                self._assert_valid_mcq(mcq, expected_level=test_diff)

    def test_comprehensive_matrix_400_runs(self):
        """Test all 16 patterns x 5 variants x 5 difficulty levels = 400 runs."""
        count = 0
        for name, pid, func in self.PATTERN_FUNCTIONS:
            variants = DAY4_PATTERNS_METADATA[pid]["variants"]
            for variant in variants:
                for diff in [1, 2, 3, 4, 5]:
                    mcq = func(difficulty=diff, forced_variant=variant)
                    self._assert_valid_mcq(mcq, expected_level=diff, expected_variant=variant)
                    self.assertEqual(mcq["pattern_name"], name)
                    count += 1
        self.assertEqual(count, 16 * 5 * 5, "Expected exactly 400 runs in comprehensive matrix")


if __name__ == "__main__":
    unittest.main()
