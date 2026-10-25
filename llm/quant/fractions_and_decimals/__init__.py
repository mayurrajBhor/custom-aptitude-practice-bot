"""Topic: Fractions and Decimals (Patterns 5010-5024)."""

from typing import Any, Dict, List, Optional, Tuple, Union

from .fraction_basics import generate_fraction_basics
from .mixed_number_conversion import generate_mixed_number_conversion
from .equivalent_fractions import generate_equivalent_fractions
from .fraction_simplification import generate_fraction_simplification
from .fraction_comparison import generate_fraction_comparison
from .fraction_addition import generate_fraction_addition
from .fraction_subtraction import generate_fraction_subtraction
from .fraction_multiplication import generate_fraction_multiplication
from .fraction_division import generate_fraction_division
from .fraction_of_quantity import generate_fraction_of_quantity
from .decimal_basics import generate_decimal_basics
from .decimal_to_fraction import generate_decimal_to_fraction
from .fraction_to_decimal import generate_fraction_to_decimal
from .fraction_to_percentage import generate_fraction_to_percentage
from .decimal_to_percentage import generate_decimal_to_percentage

fraction_basics = generate_fraction_basics
mixed_number_conversion = generate_mixed_number_conversion
equivalent_fractions = generate_equivalent_fractions
fraction_simplification = generate_fraction_simplification
fraction_comparison = generate_fraction_comparison
fraction_addition = generate_fraction_addition
fraction_subtraction = generate_fraction_subtraction
fraction_multiplication = generate_fraction_multiplication
fraction_division = generate_fraction_division
fraction_of_quantity = generate_fraction_of_quantity
decimal_basics = generate_decimal_basics
decimal_to_fraction = generate_decimal_to_fraction
fraction_to_decimal = generate_fraction_to_decimal
fraction_to_percentage = generate_fraction_to_percentage
decimal_to_percentage = generate_decimal_to_percentage

DAY2_PATTERNS_METADATA: Dict[Union[int, str], Dict[str, Any]] = {
    5010: {
        "id": 5010,
        "name": "fraction_basics",
        "description": "Understanding numerator, denominator, division interpretation, and proper/improper/mixed fraction identification.",
        "variants": ["identify_terms", "division_interpretation", "classify_fraction", "shaded_parts_concept"],
    },
    5011: {
        "id": 5011,
        "name": "mixed_number_conversion",
        "description": "Converting mixed numbers to improper fractions (Ac+b)/c and improper fractions to mixed numbers.",
        "variants": ["mixed_to_improper", "improper_to_mixed"],
    },
    5012: {
        "id": 5012,
        "name": "equivalent_fractions",
        "description": "Finding equivalent fractions, missing numerators/denominators (e.g. 3/5 = x/20), and scale factor identification.",
        "variants": ["missing_numerator", "missing_denominator", "find_equivalent", "scale_factor"],
    },
    5013: {
        "id": 5013,
        "name": "fraction_simplification",
        "description": "Reducing fractions to lowest terms, identifying already simplified fractions, and using the GCD.",
        "variants": ["reduce_lowest_terms", "identify_simplified", "gcd_simplification"],
    },
    5014: {
        "id": 5014,
        "name": "fraction_comparison",
        "description": "Comparing fractions with like denominators, like numerators, cross-multiplication, and ordering sets of fractions.",
        "variants": ["same_denominator", "same_numerator", "cross_multiplication", "ordering"],
    },
    5015: {
        "id": 5015,
        "name": "fraction_addition",
        "description": "Adding fractions with same or different denominators using LCM, and adding mixed numbers.",
        "variants": ["same_denominator", "different_denominator", "mixed_numbers_addition"],
    },
    5016: {
        "id": 5016,
        "name": "fraction_subtraction",
        "description": "Subtracting fractions with same or different denominators, and subtracting mixed numbers with borrowing.",
        "variants": ["same_denominator", "different_denominator", "mixed_numbers_borrowing"],
    },
    5017: {
        "id": 5017,
        "name": "fraction_multiplication",
        "description": "Direct fraction multiplication, cross-cancellation, whole number times fraction, and chaining multiple fractions.",
        "variants": ["direct_multiplication", "cross_cancellation", "whole_times_fraction", "multiple_fractions"],
    },
    5018: {
        "id": 5018,
        "name": "fraction_division",
        "description": "Dividing fractions using keep-change-flip (a/b * d/c), whole numbers with fractions, and mixed number division.",
        "variants": ["keep_change_flip", "whole_and_fraction", "mixed_numbers_division"],
    },
    5019: {
        "id": 5019,
        "name": "fraction_of_quantity",
        "description": "Calculating fractions of quantities (e.g. 3/5 of 100), word problems with remaining amounts, and reverse quantity problems.",
        "variants": ["direct_quantity", "word_problem", "reverse_quantity"],
    },
    5020: {
        "id": 5020,
        "name": "decimal_basics",
        "description": "Understanding tenths, hundredths, thousandths place values, and comparing and ordering decimals.",
        "variants": ["place_value", "comparing_decimals", "ordering_decimals"],
    },
    5021: {
        "id": 5021,
        "name": "decimal_to_fraction",
        "description": "Converting terminating decimals (one, two, or three decimal places) and mixed decimals to simplified fractions.",
        "variants": ["terminating_one_place", "terminating_two_places", "terminating_three_places", "mixed_decimal"],
    },
    5022: {
        "id": 5022,
        "name": "fraction_to_decimal",
        "description": "Converting terminating fractions (1/2, 1/4, 1/8, 1/5) and recurring fractions (1/3, 1/6) to decimals.",
        "variants": ["terminating_benchmark", "terminating_advanced", "recurring_fractions"],
    },
    5023: {
        "id": 5023,
        "name": "fraction_to_percentage",
        "description": "Conversions both ways between fractions and percentages using the benchmark table, including improper fractions.",
        "variants": ["fraction_to_percent", "percent_to_fraction", "improper_fraction_to_percent"],
    },
    5024: {
        "id": 5024,
        "name": "decimal_to_percentage",
        "description": "Conversions between decimals and percentages (decimal * 100 = %, % / 100 = decimal), including small and large percentages.",
        "variants": ["decimal_to_percent", "percent_to_decimal", "small_and_large_percents"],
    },
}

# Also support name-based and str-based lookups in DAY2_PATTERNS_METADATA
for _pid in list(DAY2_PATTERNS_METADATA.keys()):
    _data = DAY2_PATTERNS_METADATA[_pid]
    DAY2_PATTERNS_METADATA[str(_pid)] = _data
    DAY2_PATTERNS_METADATA[_data["name"]] = _data

DAY2_GENERATORS: Dict[Union[int, str], Any] = {
    5010: generate_fraction_basics,
    "5010": generate_fraction_basics,
    "fraction_basics": generate_fraction_basics,

    5011: generate_mixed_number_conversion,
    "5011": generate_mixed_number_conversion,
    "mixed_number_conversion": generate_mixed_number_conversion,

    5012: generate_equivalent_fractions,
    "5012": generate_equivalent_fractions,
    "equivalent_fractions": generate_equivalent_fractions,

    5013: generate_fraction_simplification,
    "5013": generate_fraction_simplification,
    "fraction_simplification": generate_fraction_simplification,

    5014: generate_fraction_comparison,
    "5014": generate_fraction_comparison,
    "fraction_comparison": generate_fraction_comparison,

    5015: generate_fraction_addition,
    "5015": generate_fraction_addition,
    "fraction_addition": generate_fraction_addition,

    5016: generate_fraction_subtraction,
    "5016": generate_fraction_subtraction,
    "fraction_subtraction": generate_fraction_subtraction,

    5017: generate_fraction_multiplication,
    "5017": generate_fraction_multiplication,
    "fraction_multiplication": generate_fraction_multiplication,

    5018: generate_fraction_division,
    "5018": generate_fraction_division,
    "fraction_division": generate_fraction_division,

    5019: generate_fraction_of_quantity,
    "5019": generate_fraction_of_quantity,
    "fraction_of_quantity": generate_fraction_of_quantity,

    5020: generate_decimal_basics,
    "5020": generate_decimal_basics,
    "decimal_basics": generate_decimal_basics,

    5021: generate_decimal_to_fraction,
    "5021": generate_decimal_to_fraction,
    "decimal_to_fraction": generate_decimal_to_fraction,

    5022: generate_fraction_to_decimal,
    "5022": generate_fraction_to_decimal,
    "fraction_to_decimal": generate_fraction_to_decimal,

    5023: generate_fraction_to_percentage,
    "5023": generate_fraction_to_percentage,
    "fraction_to_percentage": generate_fraction_to_percentage,

    5024: generate_decimal_to_percentage,
    "5024": generate_decimal_to_percentage,
    "decimal_to_percentage": generate_decimal_to_percentage,
}


class FractionsAndDecimalsMixin:
    """Mixin exposing Fractions and Decimals generators."""
    generate_fraction_basics = staticmethod(generate_fraction_basics)
    generate_mixed_number_conversion = staticmethod(generate_mixed_number_conversion)
    generate_equivalent_fractions = staticmethod(generate_equivalent_fractions)
    generate_fraction_simplification = staticmethod(generate_fraction_simplification)
    generate_fraction_comparison = staticmethod(generate_fraction_comparison)
    generate_fraction_addition = staticmethod(generate_fraction_addition)
    generate_fraction_subtraction = staticmethod(generate_fraction_subtraction)
    generate_fraction_multiplication = staticmethod(generate_fraction_multiplication)
    generate_fraction_division = staticmethod(generate_fraction_division)
    generate_fraction_of_quantity = staticmethod(generate_fraction_of_quantity)
    generate_decimal_basics = staticmethod(generate_decimal_basics)
    generate_decimal_to_fraction = staticmethod(generate_decimal_to_fraction)
    generate_fraction_to_decimal = staticmethod(generate_fraction_to_decimal)
    generate_fraction_to_percentage = staticmethod(generate_fraction_to_percentage)
    generate_decimal_to_percentage = staticmethod(generate_decimal_to_percentage)


__all__ = [
    "DAY2_GENERATORS",
    "DAY2_PATTERNS_METADATA",
    "FractionsAndDecimalsMixin",
    "generate_fraction_basics",
    "generate_mixed_number_conversion",
    "generate_equivalent_fractions",
    "generate_fraction_simplification",
    "generate_fraction_comparison",
    "generate_fraction_addition",
    "generate_fraction_subtraction",
    "generate_fraction_multiplication",
    "generate_fraction_division",
    "generate_fraction_of_quantity",
    "generate_decimal_basics",
    "generate_decimal_to_fraction",
    "generate_fraction_to_decimal",
    "generate_fraction_to_percentage",
    "generate_decimal_to_percentage",
    "fraction_basics",
    "mixed_number_conversion",
    "equivalent_fractions",
    "fraction_simplification",
    "fraction_comparison",
    "fraction_addition",
    "fraction_subtraction",
    "fraction_multiplication",
    "fraction_division",
    "fraction_of_quantity",
    "decimal_basics",
    "decimal_to_fraction",
    "fraction_to_decimal",
    "fraction_to_percentage",
    "decimal_to_percentage",
]
