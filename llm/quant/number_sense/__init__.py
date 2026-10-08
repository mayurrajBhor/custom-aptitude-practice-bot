"""Topic: Number Sense & Basic Arithmetic (Patterns 5001-5009).

Individual pattern modules:
- number_classification.py (5001)
- odd_even.py (5002)
- prime_composite.py (5003)
- factors_multiples.py (5004)
- divisibility_rules.py (5005)
- hcf_gcd.py (5006)
- lcm.py (5007)
- hcf_lcm_relation.py (5008)
- order_of_operations.py (5009)
"""

from .number_classification import generate_number_classification
from .odd_even import generate_odd_even_gmat
from .prime_composite import generate_prime_composite_gmat
from .factors_multiples import generate_factors_multiples_gmat
from .divisibility_rules import generate_divisibility_rules_gmat
from .hcf_gcd import generate_hcf_gcd_gmat
from .lcm import generate_lcm_gmat
from .hcf_lcm_relation import generate_hcf_lcm_relation_gmat
from .order_of_operations import generate_order_of_operations_gmat


DAY1_GENERATORS = {
    5001: generate_number_classification,
    "number_classification": generate_number_classification,
    5002: generate_odd_even_gmat,
    "odd_even_gmat": generate_odd_even_gmat,
    5003: generate_prime_composite_gmat,
    "prime_composite_gmat": generate_prime_composite_gmat,
    5004: generate_factors_multiples_gmat,
    "factors_multiples_gmat": generate_factors_multiples_gmat,
    5005: generate_divisibility_rules_gmat,
    "divisibility_rules_gmat": generate_divisibility_rules_gmat,
    5006: generate_hcf_gcd_gmat,
    "hcf_gcd_gmat": generate_hcf_gcd_gmat,
    5007: generate_lcm_gmat,
    "lcm_gmat": generate_lcm_gmat,
    5008: generate_hcf_lcm_relation_gmat,
    "hcf_lcm_relation_gmat": generate_hcf_lcm_relation_gmat,
    5009: generate_order_of_operations_gmat,
    "order_of_operations_gmat": generate_order_of_operations_gmat,
}

DAY1_PATTERNS_METADATA = {
    5001: {
        "id": 5001,
        "name": "number_classification",
        "title": "Number Classification",
        "description": "Natural numbers, whole numbers, integers ordering, signed operations, and sign determination.",
        "variants": [
            "natural_numbers",
            "whole_numbers",
            "integers_ordering",
            "signed_operations",
            "sign_determination",
        ],
    },
    5002: {
        "id": 5002,
        "name": "odd_even_gmat",
        "title": "Odd & Even Integers (Parity)",
        "description": "Parity rules, operations, algebraic parity, GMAT parity elimination, and consecutive integers.",
        "variants": [
            "basic_classification",
            "operations_parity",
            "algebraic_parity",
            "gmat_parity_elimination",
            "consecutive_integers",
        ],
    },
    5003: {
        "id": 5003,
        "name": "prime_composite_gmat",
        "title": "Prime & Composite Numbers",
        "description": "Prime identification, square root bound checking, composite properties, canonical factorization, and twin primes.",
        "variants": [
            "basic_prime_composite",
            "prime_checking_sqrt",
            "composite_properties",
            "canonical_factorization",
            "twin_primes",
        ],
    },
    5004: {
        "id": 5004,
        "name": "factors_multiples_gmat",
        "title": "Factors & Multiples",
        "description": "Counting factors via prime powers, factor verification, common factors, listing multiples in ranges, and factor-multiple relations.",
        "variants": [
            "list_count_factors",
            "factor_checks",
            "common_factors",
            "list_multiples",
            "factor_multiple_relations",
        ],
    },
    5005: {
        "id": 5005,
        "name": "divisibility_rules_gmat",
        "title": "Divisibility Rules",
        "description": "Divisibility rules for 2/5/10, 3/9, missing digit deduction, combined divisibility of coprimes, and elimination drills.",
        "variants": [
            "div_by_2_5_10",
            "div_by_3_9",
            "missing_digit_div",
            "combined_divisibility",
            "elimination_drills",
        ],
    },
    5006: {
        "id": 5006,
        "name": "hcf_gcd_gmat",
        "title": "HCF / GCD",
        "description": "Highest Common Factor for two and three numbers, prime factorization powers, equal grouping word problems, and remainder constraints.",
        "variants": [
            "hcf_two_numbers",
            "hcf_three_numbers",
            "prime_factorization_method",
            "equal_grouping_word_problems",
            "remainder_hcf",
        ],
    },
    5007: {
        "id": 5007,
        "name": "lcm_gmat",
        "title": "LCM (Least Common Multiple)",
        "description": "LCM for two and three numbers, prime factorization powers, repeating tolling bells, and traffic signal cycles.",
        "variants": [
            "lcm_two_numbers",
            "lcm_three_numbers",
            "prime_factorization_lcm",
            "repeating_events_bells",
            "traffic_intervals",
        ],
    },
    5008: {
        "id": 5008,
        "name": "hcf_lcm_relation_gmat",
        "title": "HCF & LCM Relationship",
        "description": "Product formula (HCF * LCM = a * b), missing number discovery, HCF from product, ratio relations, and three-number verification.",
        "variants": [
            "product_formula_find_lcm",
            "product_formula_find_missing_num",
            "find_hcf_from_product",
            "ratio_product_relation",
            "verification_drills",
        ],
    },
    5009: {
        "id": 5009,
        "name": "order_of_operations_gmat",
        "title": "Order of Operations / BODMAS",
        "description": "BODMAS fundamentals, nested parentheses/brackets, multiplication/division left-to-right rule, signed arithmetic precedence, and tricky GMAT expressions.",
        "variants": [
            "bodmas_basic",
            "nested_parentheses",
            "mult_div_left_right",
            "signed_bodmas",
            "tricky_gmat_expressions",
        ],
    },
}

for meta in list(DAY1_PATTERNS_METADATA.values()):
    DAY1_PATTERNS_METADATA[meta["name"]] = meta


class NumberSenseMixin:
    """Mixin exposing Number Sense and Basic Arithmetic generators."""
    generate_number_classification = staticmethod(generate_number_classification)
    generate_odd_even_gmat = staticmethod(generate_odd_even_gmat)
    generate_prime_composite_gmat = staticmethod(generate_prime_composite_gmat)
    generate_factors_multiples_gmat = staticmethod(generate_factors_multiples_gmat)
    generate_divisibility_rules_gmat = staticmethod(generate_divisibility_rules_gmat)
    generate_hcf_gcd_gmat = staticmethod(generate_hcf_gcd_gmat)
    generate_lcm_gmat = staticmethod(generate_lcm_gmat)
    generate_hcf_lcm_relation_gmat = staticmethod(generate_hcf_lcm_relation_gmat)
    generate_order_of_operations_gmat = staticmethod(generate_order_of_operations_gmat)


__all__ = [
    "DAY1_GENERATORS",
    "DAY1_PATTERNS_METADATA",
    "NumberSenseMixin",
    "generate_number_classification",
    "generate_odd_even_gmat",
    "generate_prime_composite_gmat",
    "generate_factors_multiples_gmat",
    "generate_divisibility_rules_gmat",
    "generate_hcf_gcd_gmat",
    "generate_lcm_gmat",
    "generate_hcf_lcm_relation_gmat",
    "generate_order_of_operations_gmat",
]
