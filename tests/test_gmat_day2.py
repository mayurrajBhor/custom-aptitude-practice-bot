"""
Unit tests for Day 2 of the GMAT Practice Engine: Fractions and Decimals.
Covers Patterns 5010 through 5024.
"""

import unittest
from typing import Any, Dict

from llm.gmat.common import clamp_level
from llm.gmat.mistakes import MISTAKE_CATEGORIES
from llm.gmat.day2_fractions import (
    DAY2_GENERATORS,
    DAY2_PATTERNS_METADATA,
    generate_fraction_basics,
    generate_mixed_number_conversion,
    generate_equivalent_fractions,
    generate_fraction_simplification,
    generate_fraction_comparison,
    generate_fraction_addition,
    generate_fraction_subtraction,
    generate_fraction_multiplication,
    generate_fraction_division,
    generate_fraction_of_quantity,
    generate_decimal_basics,
    generate_decimal_to_fraction,
    generate_fraction_to_decimal,
    generate_fraction_to_percentage,
    generate_decimal_to_percentage,
)


class TestGMATDay2(unittest.TestCase):
    """Thorough test suite for Day 2 Fractions & Decimals generators and metadata."""

    def test_patterns_metadata_completeness(self):
        """Verify that DAY2_PATTERNS_METADATA contains all patterns 5010-5024 with valid schema."""
        expected_patterns = [
            (5010, "fraction_basics"),
            (5011, "mixed_number_conversion"),
            (5012, "equivalent_fractions"),
            (5013, "fraction_simplification"),
            (5014, "fraction_comparison"),
            (5015, "fraction_addition"),
            (5016, "fraction_subtraction"),
            (5017, "fraction_multiplication"),
            (5018, "fraction_division"),
            (5019, "fraction_of_quantity"),
            (5020, "decimal_basics"),
            (5021, "decimal_to_fraction"),
            (5022, "fraction_to_decimal"),
            (5023, "fraction_to_percentage"),
            (5024, "decimal_to_percentage"),
        ]

        for pid, name in expected_patterns:
            self.assertIn(pid, DAY2_PATTERNS_METADATA, f"Pattern {pid} missing from metadata")
            self.assertIn(str(pid), DAY2_PATTERNS_METADATA, f"Pattern '{pid}' missing from metadata")
            self.assertIn(name, DAY2_PATTERNS_METADATA, f"Pattern '{name}' missing from metadata")

            meta = DAY2_PATTERNS_METADATA[pid]
            self.assertEqual(meta["id"], pid)
            self.assertEqual(meta["name"], name)
            self.assertTrue(isinstance(meta["description"], str) and len(meta["description"]) > 10)
            self.assertTrue(isinstance(meta["variants"], list) and len(meta["variants"]) >= 2)

    def test_generators_registry_keys(self):
        """Ensure DAY2_GENERATORS maps pattern IDs (int, str) and names to callables."""
        for pid in range(5010, 5025):
            self.assertIn(pid, DAY2_GENERATORS, f"Integer key {pid} missing from DAY2_GENERATORS")
            self.assertIn(str(pid), DAY2_GENERATORS, f"String key '{pid}' missing from DAY2_GENERATORS")
            name = DAY2_PATTERNS_METADATA[pid]["name"]
            self.assertIn(name, DAY2_GENERATORS, f"Name key '{name}' missing from DAY2_GENERATORS")

            self.assertTrue(callable(DAY2_GENERATORS[pid]))
            self.assertTrue(callable(DAY2_GENERATORS[str(pid)]))
            self.assertTrue(callable(DAY2_GENERATORS[name]))

    def _validate_mcq_structure(self, q: Dict[str, Any], expected_level: int, expected_pattern: str):
        """Helper to assert strict GMAT question quality standards."""
        self.assertIsInstance(q, dict)
        self.assertTrue(q.get("question_text"), "Question text must not be empty")

        options = q.get("options")
        self.assertIsInstance(options, list, "Options must be a list")
        self.assertEqual(len(options), 4, f"Options must have exactly 4 items, got {len(options)}")
        self.assertEqual(
            len(set(options)),
            4,
            f"All 4 options must be strictly unique. Found duplicates in: {options}",
        )

        idx = q.get("correct_option_index")
        self.assertIsInstance(idx, int)
        self.assertTrue(0 <= idx < 4, f"correct_option_index must be between 0 and 3, got {idx}")

        correct_choice = options[idx]
        self.assertTrue(str(correct_choice).strip(), "Correct option text must not be empty")

        explanation = q.get("explanation")
        self.assertTrue(explanation, "Explanation must not be empty")
        self.assertIn(str(correct_choice).strip().lower(), explanation.lower(), "Explanation should reference correct answer")

        diff = q.get("difficulty")
        self.assertEqual(diff, clamp_level(expected_level))

        # Check trap_map categories against MISTAKE_CATEGORIES if present
        trap_map = q.get("trap_map", {})
        self.assertIsInstance(trap_map, dict)
        for trap_opt, trap_cat in trap_map.items():
            self.assertIn(
                trap_cat,
                MISTAKE_CATEGORIES,
                f"Invalid mistake category '{trap_cat}' in trap_map for option '{trap_opt}'",
            )

        self.assertEqual(q.get("pattern_name"), expected_pattern)
        self.assertTrue(q.get("subvariant"), "Subvariant must be populated")

    def test_all_15_generators_difficulties(self):
        """Test each of the 15 generators across difficulties Level 1, 3, and 5."""
        all_generators = [
            (generate_fraction_basics, "fraction_basics"),
            (generate_mixed_number_conversion, "mixed_number_conversion"),
            (generate_equivalent_fractions, "equivalent_fractions"),
            (generate_fraction_simplification, "fraction_simplification"),
            (generate_fraction_comparison, "fraction_comparison"),
            (generate_fraction_addition, "fraction_addition"),
            (generate_fraction_subtraction, "fraction_subtraction"),
            (generate_fraction_multiplication, "fraction_multiplication"),
            (generate_fraction_division, "fraction_division"),
            (generate_fraction_of_quantity, "fraction_of_quantity"),
            (generate_decimal_basics, "decimal_basics"),
            (generate_decimal_to_fraction, "decimal_to_fraction"),
            (generate_fraction_to_decimal, "fraction_to_decimal"),
            (generate_fraction_to_percentage, "fraction_to_percentage"),
            (generate_decimal_to_percentage, "decimal_to_percentage"),
        ]

        for gen_fn, pat_name in all_generators:
            for level in [1, 3, 5]:
                q = gen_fn(difficulty=level)
                self._validate_mcq_structure(q, expected_level=level, expected_pattern=pat_name)

    def test_all_variants_can_be_forced(self):
        """Test that every variant across all 15 patterns can be explicitly forced."""
        for pid in range(5010, 5025):
            meta = DAY2_PATTERNS_METADATA[pid]
            gen_fn = DAY2_GENERATORS[pid]
            pat_name = meta["name"]
            variants = meta["variants"]

            for variant in variants:
                q = gen_fn(difficulty=3, forced_variant=variant)
                self._validate_mcq_structure(q, expected_level=3, expected_pattern=pat_name)
                self.assertEqual(
                    q["subvariant"],
                    variant,
                    f"Generator for pattern {pid} ({pat_name}) did not honor forced_variant='{variant}'",
                )

    def test_repetition_stability(self):
        """Run each pattern multiple times to ensure no random edge crashes or duplicate options."""
        for pid in range(5010, 5025):
            gen_fn = DAY2_GENERATORS[pid]
            pat_name = DAY2_PATTERNS_METADATA[pid]["name"]
            for i in range(50):
                level = 1 + (i % 5)
                q = gen_fn(difficulty=level)
                self._validate_mcq_structure(q, expected_level=level, expected_pattern=pat_name)

    def test_boundary_inputs_and_fallbacks(self):
        """Test out-of-range difficulty and invalid forced_variant fallbacks."""
        for pid in range(5010, 5025):
            gen_fn = DAY2_GENERATORS[pid]
            pat_name = DAY2_PATTERNS_METADATA[pid]["name"]
            meta = DAY2_PATTERNS_METADATA[pid]

            # Out of bounds difficulty below 1
            q_low = gen_fn(difficulty=-5)
            self.assertEqual(q_low["difficulty"], 1)
            self._validate_mcq_structure(q_low, expected_level=1, expected_pattern=pat_name)

            # Out of bounds difficulty above 5
            q_high = gen_fn(difficulty=99)
            self.assertEqual(q_high["difficulty"], 5)
            self._validate_mcq_structure(q_high, expected_level=5, expected_pattern=pat_name)

            # Invalid forced_variant fallback
            q_invalid_var = gen_fn(difficulty=2, forced_variant="non_existent_variant_name")
            self.assertIn(q_invalid_var["subvariant"], meta["variants"])
            self._validate_mcq_structure(q_invalid_var, expected_level=2, expected_pattern=pat_name)


if __name__ == "__main__":
    unittest.main()
