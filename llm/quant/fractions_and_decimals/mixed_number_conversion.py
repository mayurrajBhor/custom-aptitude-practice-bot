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

def generate_mixed_number_conversion(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["mixed_to_improper", "improper_to_mixed"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "mixed_to_improper":
        if level <= 2:
            w = random.randint(1, 4)
            d = random.randint(2, 6)
            n = random.randint(1, d - 1)
        elif level <= 4:
            w = random.randint(4, 9)
            d = random.randint(5, 12)
            n = random.randint(1, d - 1)
        else:
            w = random.randint(11, 20)
            d = random.randint(7, 16)
            n = random.randint(1, d - 1)

        while math.gcd(n, d) > 1:
            n = random.randint(1, d - 1)

        improper_num = w * d + n
        correct = f"{improper_num}/{d}"

        candidates = [
            (f"{w * n + d}/{d}", "formula_selection_mistake"),
            (f"{w + n}/{d}", "conceptual_mistake"),
            (f"{improper_num + 1}/{d}", "arithmetic_mistake"),
            (f"{improper_num - 1}/{d}", "arithmetic_mistake"),
            (f"{d}/{improper_num}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the mixed number {w} {n}/{d} into an improper fraction."
        expl = (
            f"To convert a mixed number W n/d to an improper fraction:\n"
            f"Numerator = (Whole × Denominator) + Numerator = ({w} × {d}) + {n} = {w * d} + {n} = {improper_num}.\n"
            f"Denominator stays the same: {d}.\n"
            f"Thus, {w} {n}/{d} = {correct}."
        )

    else:  # improper_to_mixed
        if level <= 2:
            w = random.randint(1, 4)
            d = random.randint(2, 5)
            r = random.randint(1, d - 1)
        elif level <= 4:
            w = random.randint(4, 9)
            d = random.randint(5, 11)
            r = random.randint(1, d - 1)
        else:
            w = random.randint(11, 20)
            d = random.randint(7, 17)
            r = random.randint(1, d - 1)

        while math.gcd(r, d) > 1:
            r = random.randint(1, d - 1)

        m = w * d + r
        correct = f"{w} {r}/{d}"

        candidates = [
            (f"{r} {w}/{d}", "careless_mistake"),
            (f"{w + 1} {r}/{d}", "arithmetic_mistake"),
            (f"{w - 1} {r + 1}/{d}", "arithmetic_mistake"),
            (f"{w} {d - r}/{d}", "formula_selection_mistake"),
            (f"{w + r}/{d}", "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the improper fraction {m}/{d} into a mixed number."
        expl = (
            f"To convert an improper fraction M/d to a mixed number:\n"
            f"1. Divide {m} by {d}: {m} ÷ {d} = {w} with a remainder of {r} (since {w} × {d} = {w * d}, and {m} - {w * d} = {r}).\n"
            f"2. The quotient ({w}) is the whole number part, and remainder ({r}) becomes the new numerator over {d}.\n"
            f"Thus, {m}/{d} = {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="mixed_number_conversion",
        subvariant=variant,
    )

