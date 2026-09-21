import os
import unittest
from fastapi.testclient import TestClient

os.environ.setdefault("GROQ_API_KEY", "test-key")

import web_app
from local_catalog import get_local_catalog_payload, get_local_pattern, is_local_pattern_id
from llm.generator import generator


class NumberPropertiesAndFactorsTests(unittest.TestCase):
    def setUp(self):
        web_app.SESSIONS.clear()
        self.client = TestClient(web_app.app)

    def test_catalog_contains_number_properties_and_factors_topics(self):
        catalog = get_local_catalog_payload()
        quant_cat = next((c for c in catalog if c["name"] == "Quant"), None)
        self.assertIsNotNone(quant_cat, "Quant category missing from local catalog")

        topic_names = [t["name"] for t in quant_cat["topics"]]
        self.assertIn("Number properties", topic_names)
        self.assertIn("Factors & multiples", topic_names)

        num_prop = next(t for t in quant_cat["topics"] if t["name"] == "Number properties")
        factors_topic = next(t for t in quant_cat["topics"] if t["name"] == "Factors & multiples")

        self.assertEqual(len(num_prop["patterns"]), 2)
        self.assertEqual(len(factors_topic["patterns"]), 5)

        pattern_ids = [p["id"] for p in num_prop["patterns"]] + [p["id"] for p in factors_topic["patterns"]]
        expected_ids = [4001, 4002, 4003, 4004, 4005, 4006, 4007]
        self.assertEqual(pattern_ids, expected_ids)

        for pat in num_prop["patterns"] + factors_topic["patterns"]:
            self.assertEqual(pat["variant_count"], 5)
            self.assertEqual(len(pat["variant_names"]), 5)
            self.assertTrue(is_local_pattern_id(pat["id"]))

    def test_fast_catalog_api_exposes_new_patterns(self):
        response = self.client.get("/api/catalog/fast")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        quant = next((c for c in payload["categories"] if c["name"] == "Quant"), None)
        self.assertIsNotNone(quant)

        topics_by_name = {t["name"]: t for t in quant["topics"]}
        self.assertIn("Number properties", topics_by_name)
        self.assertIn("Factors & multiples", topics_by_name)

        np_patterns = {p["name"]: p for p in topics_by_name["Number properties"]["patterns"]}
        fm_patterns = {p["name"]: p for p in topics_by_name["Factors & multiples"]["patterns"]}

        self.assertIn("Odd/even", np_patterns)
        self.assertIn("Prime/composite", np_patterns)
        self.assertIn("Factors", fm_patterns)
        self.assertIn("Multiples", fm_patterns)
        self.assertIn("Prime factorization", fm_patterns)
        self.assertIn("HCF/GCD", fm_patterns)
        self.assertIn("LCM", fm_patterns)

    def test_pattern_name_mapping_in_generator(self):
        expected_mappings = {
            "Odd/even": "odd_even",
            "odd/even": "odd_even",
            "Odd and even properties": "odd_even",
            "Prime/composite": "prime_composite",
            "prime/composite properties": "prime_composite",
            "Factors": "factors",
            "factors and divisors": "factors",
            "Multiples": "multiples",
            "multiples and divisibility patterns": "multiples",
            "Prime factorization": "prime_factorization",
            "HCF/GCD": "hcf_gcd",
            "highest common factor (hcf / gcd)": "hcf_gcd",
            "LCM": "lcm",
            "least common multiple (lcm)": "lcm",
        }
        for name, expected_type in expected_mappings.items():
            self.assertEqual(
                generator._get_hybrid_type(name),
                expected_type,
                f"Failed mapping for '{name}'"
            )

    def test_all_35_subtypes_generation(self):
        subtypes_by_pattern = {
            "odd_even": [
                "parity_arithmetic",
                "algebraic_parity",
                "consecutive_integers",
                "power_and_exponents",
                "word_problem_parity",
            ],
            "prime_composite": [
                "prime_identification",
                "coprime_pairs",
                "prime_ranges_and_counting",
                "composite_properties",
                "twin_primes_and_triplets",
            ],
            "factors": [
                "total_number_of_factors",
                "sum_of_factors",
                "odd_and_even_factors",
                "factor_pairs_and_products",
                "perfect_square_factors",
            ],
            "multiples": [
                "counting_multiples_in_range",
                "common_multiples_and_intervals",
                "either_or_multiples",
                "consecutive_multiples_sum",
                "word_problems_multiples",
            ],
            "prime_factorization": [
                "canonical_decomposition",
                "highest_power_in_factorial",
                "missing_factor_for_perfect_power",
                "distinct_prime_factors",
                "algebraic_factorization",
            ],
            "hcf_gcd": [
                "euclidean_algorithm",
                "prime_factorization_hcf",
                "fractions_hcf",
                "largest_divisor_with_remainders",
                "word_problems_tiling",
            ],
            "lcm": [
                "prime_factorization_lcm",
                "fractions_lcm",
                "product_formula_relation",
                "smallest_number_with_remainders",
                "word_problems_bells",
            ],
        }

        for base_type, subtypes in subtypes_by_pattern.items():
            for subtype in subtypes:
                variant_key = f"{base_type}::{subtype}"
                for difficulty in [1, 2, 3]:
                    result = generator._generate_hybrid(variant_key, difficulty=difficulty)
                    self.assertIsNotNone(result, f"Generator returned None for {variant_key}")
                    self.assertIn("question_text", result, f"Missing question_text for {variant_key}")
                    self.assertTrue(bool(result["question_text"].strip()))
                    self.assertIn("options", result, f"Missing options for {variant_key}")
                    self.assertEqual(len(result["options"]), 4, f"Options != 4 for {variant_key}")
                    self.assertEqual(len(set(result["options"])), 4, f"Duplicate options in {variant_key}: {result['options']}")
                    self.assertIn("correct_option_index", result, f"Missing correct_option_index for {variant_key}")
                    self.assertIn(result["correct_option_index"], [0, 1, 2, 3])
                    self.assertIn("explanation", result, f"Missing explanation for {variant_key}")
                    self.assertTrue(bool(result["explanation"].strip()))

    def test_practice_session_with_number_properties_patterns(self):
        for pattern_id in [4001, 4002, 4003, 4004, 4005, 4006, 4007]:
            response = self.client.post(
                "/api/session/start",
                json={
                    "pattern_ids": [pattern_id],
                    "mode": "quick",
                    "target_count": 2,
                },
            )
            self.assertEqual(response.status_code, 200, f"Failed starting session for pattern {pattern_id}: {response.text}")
            session_id = response.json()["session_id"]

            # Next question
            next_res = self.client.post(f"/api/session/{session_id}/next")
            self.assertEqual(next_res.status_code, 200)
            q_data = next_res.json()["question"]
            self.assertEqual(q_data["question_number"], 1)
            self.assertEqual(len(q_data["options"]), 4)

            # Answer question
            ans_res = self.client.post(
                f"/api/session/{session_id}/answer",
                json={"answer_index": q_data["correct_option_index"]},
            )
            self.assertEqual(ans_res.status_code, 200)
            self.assertTrue(ans_res.json()["is_correct"])

    def test_explicit_variant_selection_for_new_patterns(self):
        pattern_id = 4007 # LCM
        variants = generator.get_hybrid_variants("LCM")
        self.assertEqual(len(variants), 5)
        chosen = [variants[0], variants[4]] # prime_factorization_lcm and word_problems_bells

        response = self.client.post(
            "/api/session/start",
            json={
                "pattern_ids": [pattern_id],
                "mode": "quick",
                "target_count": 2,
                "variant_selection": {str(pattern_id): chosen},
            },
        )
        self.assertEqual(response.status_code, 200)
        session = web_app.SESSIONS[response.json()["session_id"]]
        hybrid_types = {item.get("hybrid_type") for item in session["items"] if item.get("hybrid_type")}
        self.assertEqual(hybrid_types, set(chosen))


if __name__ == "__main__":
    unittest.main()
