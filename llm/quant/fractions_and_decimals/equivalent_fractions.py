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

def generate_equivalent_fractions(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["missing_numerator", "missing_denominator", "find_equivalent", "scale_factor"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "missing_numerator":
        if level <= 2:
            a = random.randint(2, 5)
            b = random.randint(a + 1, 9)
            k = random.randint(2, 5)
        elif level <= 4:
            a = random.randint(3, 11)
            b = random.randint(a + 1, 15)
            k = random.randint(4, 9)
        else:
            a = random.randint(8, 19)
            b = random.randint(a + 1, 25)
            k = random.randint(7, 15)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        d = b * k
        x = a * k
        correct = str(x)

        candidates = [
            (str(a + (d - b)), "conceptual_mistake"),
            (str(a * (k + 1)), "arithmetic_mistake"),
            (str(a * max(1, k - 1)), "arithmetic_mistake"),
            (str(b * k), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Find the value of x if: {a}/{b} = x/{d}"
        expl = (
            f"Step 1: Determine the scale factor between the denominators: {d} ÷ {b} = {k}.\n"
            f"Step 2: Equivalent fractions require multiplying both numerator and denominator by the same factor.\n"
            f"Step 3: Multiply the numerator by {k}: x = {a} × {k} = {x}."
        )

    elif variant == "missing_denominator":
        if level <= 2:
            a = random.randint(2, 5)
            b = random.randint(a + 1, 9)
            k = random.randint(2, 5)
        elif level <= 4:
            a = random.randint(3, 11)
            b = random.randint(a + 1, 15)
            k = random.randint(4, 9)
        else:
            a = random.randint(7, 17)
            b = random.randint(a + 1, 23)
            k = random.randint(6, 14)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        c = a * k
        x = b * k
        correct = str(x)

        candidates = [
            (str(b + (c - a)), "conceptual_mistake"),
            (str(b * (k + 1)), "arithmetic_mistake"),
            (str(b * max(1, k - 1)), "arithmetic_mistake"),
            (str(c * a), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Find the value of x if: {a}/{b} = {c}/x"
        expl = (
            f"Step 1: Determine the multiplier applied to the numerator: {c} ÷ {a} = {k}.\n"
            f"Step 2: Multiply the denominator by the same scale factor {k}: x = {b} × {k} = {x}."
        )

    elif variant == "find_equivalent":
        if level <= 2:
            a = random.randint(2, 4)
            b = random.randint(a + 1, 7)
            k = random.randint(2, 4)
        else:
            a = random.randint(3, 9)
            b = random.randint(a + 1, 13)
            k = random.randint(3, 8)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        correct = f"{a * k}/{b * k}"
        candidates = [
            (f"{a + k}/{b + k}", "conceptual_mistake"),
            (f"{a * k}/{b}", "formula_selection_mistake"),
            (f"{a}/{b * k}", "formula_selection_mistake"),
            (f"{b * k}/{a * k}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Which of the following fractions is equivalent to {a}/{b}?"
        expl = (
            f"To produce an equivalent fraction, both the numerator and denominator must be multiplied "
            f"by the exact same non-zero integer.\n"
            f"Multiplying both numerator and denominator by {k} yields ({a} × {k}) / ({b} × {k}) = {correct}.\n"
            f"Note: Adding {k} to both top and bottom (e.g. {a+k}/{b+k}) alters the fraction's value and is a common trap."
        )

    else:  # scale_factor
        a = random.randint(2, 7)
        b = random.randint(a + 1, 12)
        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)
        k = random.randint(3, 9) if level <= 3 else random.randint(11, 25)
        c = a * k
        d = b * k
        correct = str(k)
        candidates = [
            (str(k + 1), "arithmetic_mistake"),
            (str(max(1, k - 1)), "arithmetic_mistake"),
            (str(c - a), "conceptual_mistake"),
            (str(d - b), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = (
            f"By what factor were both the numerator and denominator of {a}/{b} multiplied "
            f"to create the equivalent fraction {c}/{d}?"
        )
        expl = (
            f"Scale factor = {c} ÷ {a} = {k} (and {d} ÷ {b} = {k}).\n"
            f"Thus, the scale factor used is {k}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="equivalent_fractions",
        subvariant=variant,
    )

