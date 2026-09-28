"""Tests for Day 1: GMAT Practice Engine - Arithmetic Foundations (Patterns 5001-5009)"""

import unittest
from llm.gmat.day1_arithmetic import (
    DAY1_GENERATORS,
    DAY1_PATTERNS_METADATA,
    generate_number_classification,
    generate_odd_even_gmat,
    generate_prime_composite_gmat,
    generate_factors_multiples_gmat,
    generate_divisibility_rules_gmat,
    generate_hcf_gcd_gmat,
    generate_lcm_gmat,
    generate_hcf_lcm_relation_gmat,
    generate_order_of_operations_gmat,
)


class TestGMATDay1Arithmetic(unittest.TestCase):
    def setUp(self):
        self.generators = [
            (5001, "number_classification", generate_number_classification),
            (5002, "odd_even_gmat", generate_odd_even_gmat),
            (5003, "prime_composite_gmat", generate_prime_composite_gmat),
            (5004, "factors_multiples_gmat", generate_factors_multiples_gmat),
            (5005, "divisibility_rules_gmat", generate_divisibility_rules_gmat),
            (5006, "hcf_gcd_gmat", generate_hcf_gcd_gmat),
            (5007, "lcm_gmat", generate_lcm_gmat),
            (5008, "hcf_lcm_relation_gmat", generate_hcf_lcm_relation_gmat),
            (5009, "order_of_operations_gmat", generate_order_of_operations_gmat),
        ]

    def _verify_mcq_structure(self, mcq, expected_variant=None, expected_difficulty=None):
        self.assertIsInstance(mcq, dict)
        self.assertIn("question_text", mcq)
        self.assertTrue(len(mcq["question_text"].strip()) > 0, "question_text should not be empty")

        self.assertIn("options", mcq)
        options = mcq["options"]
        self.assertEqual(len(options), 4, f"Options count should be 4, got {len(options)}")
        self.assertEqual(len(set(options)), 4, f"Options must all be distinct: {options}")

        self.assertIn("correct_option_index", mcq)
        idx = mcq["correct_option_index"]
        self.assertIsInstance(idx, int)
        self.assertTrue(0 <= idx < 4, f"correct_option_index {idx} out of range [0, 3]")

        self.assertIn("explanation", mcq)
        self.assertTrue(len(mcq["explanation"].strip()) > 0, "explanation should not be empty")

        self.assertIn("difficulty", mcq)
        self.assertTrue(1 <= mcq["difficulty"] <= 5, "difficulty should be clamped between 1 and 5")
        if expected_difficulty is not None:
            self.assertEqual(mcq["difficulty"], max(1, min(5, expected_difficulty)))

        self.assertIn("trap_map", mcq)
        self.assertIsInstance(mcq["trap_map"], dict)

        if expected_variant:
            self.assertEqual(mcq.get("subvariant"), expected_variant)

    def test_metadata_registry(self):
        """Test that DAY1_PATTERNS_METADATA is properly configured with 9 patterns."""
        for pattern_id in range(5001, 5010):
            self.assertIn(pattern_id, DAY1_PATTERNS_METADATA)
            meta = DAY1_PATTERNS_METADATA[pattern_id]
            self.assertEqual(meta["id"], pattern_id)
            self.assertIn("name", meta)
            self.assertIn("title", meta)
            self.assertIn("description", meta)
            self.assertIn("variants", meta)
            self.assertEqual(len(meta["variants"]), 5, f"Pattern {pattern_id} should have 5 variants")

            # Check string lookup
            name = meta["name"]
            self.assertIn(name, DAY1_PATTERNS_METADATA)
            self.assertEqual(DAY1_PATTERNS_METADATA[name]["id"], pattern_id)

    def test_generators_registry(self):
        """Test that DAY1_GENERATORS exposes all 9 patterns by ID and string key."""
        for pattern_id, name, gen_fn in self.generators:
            self.assertIn(pattern_id, DAY1_GENERATORS)
            self.assertIn(name, DAY1_GENERATORS)
            self.assertEqual(DAY1_GENERATORS[pattern_id], gen_fn)
            self.assertEqual(DAY1_GENERATORS[name], gen_fn)

    def test_generators_at_multiple_difficulties(self):
        """Each generator must produce valid MCQs at Level 1, Level 3, and Level 5."""
        for pattern_id, name, gen_fn in self.generators:
            for diff in [1, 3, 5]:
                for _ in range(3):  # Run a few times for randomized subvariants
                    mcq = gen_fn(difficulty=diff)
                    self._verify_mcq_structure(mcq, expected_difficulty=diff)
                    self.assertEqual(mcq.get("pattern_name"), name)

    def test_generators_clamping(self):
        """Difficulty out-of-bounds should clamp to 1 or 5."""
        for _, _, gen_fn in self.generators:
            mcq_low = gen_fn(difficulty=-2)
            self.assertEqual(mcq_low["difficulty"], 1)

            mcq_high = gen_fn(difficulty=99)
            self.assertEqual(mcq_high["difficulty"], 5)

    def test_forced_variants_all_patterns(self):
        """Test each of the 5 variants can be explicitly forced for all 9 patterns across multiple iterations and difficulties."""
        for pattern_id, name, gen_fn in self.generators:
            meta = DAY1_PATTERNS_METADATA[pattern_id]
            variants = meta["variants"]
            self.assertEqual(len(variants), 5)
            for variant in variants:
                # Test multiple iterations per variant across difficulties 1 to 5
                for diff in range(1, 6):
                    for _ in range(5):
                        mcq = gen_fn(difficulty=diff, forced_variant=variant)
                        self._verify_mcq_structure(mcq, expected_variant=variant, expected_difficulty=diff)


if __name__ == "__main__":
    unittest.main()
