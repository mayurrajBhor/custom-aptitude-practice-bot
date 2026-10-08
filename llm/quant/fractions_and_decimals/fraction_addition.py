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

def generate_fraction_addition(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["same_denominator", "different_denominator", "mixed_numbers_addition"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "same_denominator":
        d = random.randint(5, 12)
        a = random.randint(1, d - 2)
        b = random.randint(1, d - a)
        ans = Fraction(a + b, d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a + b, 2 * d), "conceptual_mistake"),
            (_format_frac(a + b + 1, d), "arithmetic_mistake"),
            (_format_frac(abs(a - b), d), "careless_mistake"),
            (_format_frac(a * b, d), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{d} + {b}/{d}"
        expl = (
            f"Step 1: Since the denominators are identical ({d}), add the numerators directly:\n"
            f"  {a} + {b} = {a + b}.\n"
            f"Step 2: Keep the common denominator {d}: ({a} + {b})/{d} = {a + b}/{d}.\n"
            f"Step 3: Simplify if possible: {correct}."
        )

    elif variant == "different_denominator":
        if level <= 3:
            b = random.randint(2, 6)
            d = random.randint(2, 6)
            while b == d:
                d = random.randint(2, 7)
            a = random.randint(1, b - 1)
            c = random.randint(1, d - 1)
        else:
            b = random.randint(4, 10)
            d = random.randint(4, 12)
            while b == d:
                d = random.randint(4, 14)
            a = random.randint(1, b - 1)
            c = random.randint(1, d - 1)

        f1 = Fraction(a, b)
        f2 = Fraction(c, d)
        ans = f1 + f2
        correct = _format_frac(ans.numerator, ans.denominator)

        mediant = _format_frac(a + c, b + d)
        common_lcm = math.lcm(b, d)
        candidates = [
            (mediant, "conceptual_mistake"),
            (_format_frac(a + c, b * d), "formula_selection_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(ans.numerator - 1, ans.denominator), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{b} + {c}/{d}"
        expl = (
            f"Step 1: Find the least common multiple of denominators {b} and {d}: LCM({b}, {d}) = {common_lcm}.\n"
            f"Step 2: Convert to equivalent fractions with denominator {common_lcm}:\n"
            f"  {a}/{b} = {a * (common_lcm // b)}/{common_lcm}\n"
            f"  {c}/{d} = {c * (common_lcm // d)}/{common_lcm}\n"
            f"Step 3: Add numerators: {a * (common_lcm // b)} + {c * (common_lcm // d)} = {ans.numerator * (common_lcm // ans.denominator)}.\n"
            f"Step 4: Reduce to lowest terms: {correct}.\n"
            f"Common Trap: Adding top and bottom directly ({a}+{c})/({b}+{d}) = {mediant} is incorrect."
        )

    else:  # mixed_numbers_addition
        w1 = random.randint(1, 4)
        w2 = random.randint(1, 4)
        b = random.choice([2, 3, 4, 5])
        d = random.choice([2, 3, 4, 5])
        while b == d:
            d = random.choice([2, 3, 4, 6])
        a = random.randint(1, b - 1)
        c = random.randint(1, d - 1)

        f_total = w1 + Fraction(a, b) + w2 + Fraction(c, d)
        wh = f_total.numerator // f_total.denominator
        rem = f_total.numerator % f_total.denominator
        correct = _format_mixed(wh, rem, f_total.denominator)

        candidates = [
            (_format_mixed(w1 + w2, a + c, b + d), "conceptual_mistake"),
            (_format_mixed(wh + 1, rem, f_total.denominator), "arithmetic_mistake"),
            (_format_mixed(wh - 1, rem, f_total.denominator), "arithmetic_mistake"),
            (_format_frac(f_total.numerator, f_total.denominator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {w1} {a}/{b} + {w2} {c}/{d} (express as a mixed number in simplest form)"
        expl = (
            f"Step 1: Add the whole numbers: {w1} + {w2} = {w1 + w2}.\n"
            f"Step 2: Add the fractions: {a}/{b} + {c}/{d}.\n"
            f"  LCM({b}, {d}) = {math.lcm(b, d)}.\n"
            f"  Sum of fractions = {Fraction(a, b) + Fraction(c, d)}.\n"
            f"Step 3: Combine whole number and fraction: total = {f_total} = {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_addition",
        subvariant=variant,
    )

