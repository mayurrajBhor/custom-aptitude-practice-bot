import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

from llm.common import (
    GMAT_BENCHMARK_FRACTIONS,
    clamp_level,
    gcd,
    lcm,
    make_mcq,
    make_options,
)
from .common import _clean_distractors, _format_frac, _format_mixed

def generate_decimal_basics(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["place_value", "comparing_decimals", "ordering_decimals"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "place_value":
        d1 = random.randint(1, 9)
        d2 = random.randint(1, 9)
        d3 = random.randint(1, 9)
        d4 = random.randint(1, 9)
        num_str = f"3.{d1}{d2}{d3}{d4}"

        places = [
            (d1, "Tenths (0.1)"),
            (d2, "Hundredths (0.01)"),
            (d3, "Thousandths (0.001)"),
            (d4, "Ten-thousandths (0.0001)"),
        ]
        target_digit, correct = random.choice(places)

        all_names = ["Tenths (0.1)", "Hundredths (0.01)", "Thousandths (0.001)", "Ten-thousandths (0.0001)"]
        candidates = [(name, "conceptual_mistake") for name in all_names if name != correct]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"In the number {num_str}, what is the place value of the digit {target_digit}?"
        expl = (
            f"In decimal place notation to the right of the decimal point:\n"
            f"- 1st place = Tenths (0.1)\n"
            f"- 2nd place = Hundredths (0.01)\n"
            f"- 3rd place = Thousandths (0.001)\n"
            f"- 4th place = Ten-thousandths (0.0001)\n"
            f"Here, {target_digit} is in the {correct.split()[0].lower()} position."
        )

    elif variant == "comparing_decimals":
        # The classic trap: longer decimals are not necessarily larger!
        decimals = ["0.08", "0.8", "0.088", "0.0089"]
        correct = "0.8"
        candidates = [
            ("0.088", "conceptual_mistake"),
            ("0.0089", "conceptual_mistake"),
            ("0.08", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Which of the following decimals has the greatest numerical value?"
        expl = (
            f"To compare decimals, align them by the decimal point or pad with trailing zeros:\n"
            f"  0.0800\n"
            f"  0.8000  <-- largest (8 tenths)\n"
            f"  0.0880\n"
            f"  0.0089\n"
            f"0.8 has 8 tenths, whereas all other choices have 0 tenths. "
            f"Common Trap: Believing 0.0089 is larger because 89 is a bigger number is incorrect."
        )

    else:  # ordering_decimals
        decimals = [0.05, 0.5, 0.055, 0.505]
        decimals_sorted = sorted(decimals)
        correct = " < ".join(str(x) for x in decimals_sorted)
        reversed_order = " < ".join(str(x) for x in reversed(decimals_sorted))

        candidates = [
            (reversed_order, "careless_mistake"),
            ("0.05 < 0.5 < 0.055 < 0.505", "conceptual_mistake"),
            ("0.055 < 0.05 < 0.5 < 0.505", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Which of the following arranges the decimals 0.5, 0.05, 0.505, and 0.055 in ascending order?"
        expl = (
            f"Padding each decimal to 3 places:\n"
            f"  0.050, 0.055, 0.500, 0.505\n"
            f"Ordering from smallest to largest yields {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_basics",
        subvariant=variant,
    )

