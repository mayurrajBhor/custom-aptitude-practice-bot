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

def generate_fraction_subtraction(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["same_denominator", "different_denominator", "mixed_numbers_borrowing"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "same_denominator":
        d = random.randint(5, 13)
        b = random.randint(1, d - 3)
        a = random.randint(b + 1, d - 1)
        ans = Fraction(a - b, d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a + b, d), "sign_mistake"),
            (_format_frac(a - b, 2 * d), "conceptual_mistake"),
            (_format_frac(max(1, a - b + 1), d), "arithmetic_mistake"),
            (_format_frac(b, d), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{d} - {b}/{d}"
        expl = (
            f"Step 1: Denominators are the same ({d}), so subtract numerators: {a} - {b} = {a - b}.\n"
            f"Step 2: Place over common denominator: {a - b}/{d}.\n"
            f"Step 3: Simplify if necessary: {correct}."
        )

    elif variant == "different_denominator":
        b = random.randint(2, 6)
        d = random.randint(2, 7)
        while b == d:
            d = random.randint(2, 8)
        a = random.randint(1, b - 1)
        c = random.randint(1, d - 1)

        f1 = Fraction(a, b)
        f2 = Fraction(c, d)
        if f1 < f2:
            a, c = c, a
            b, d = d, b
            f1, f2 = f2, f1
        elif f1 == f2:
            a += 1
            f1 = Fraction(a, b)

        ans = f1 - f2
        correct = _format_frac(ans.numerator, ans.denominator)
        common_lcm = math.lcm(b, d)

        candidates = [
            (_format_frac(abs(a - c), abs(b - d) if b != d else b), "conceptual_mistake"),
            (_format_frac((f1 + f2).numerator, (f1 + f2).denominator), "sign_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(abs(a - c), common_lcm), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{b} - {c}/{d}"
        expl = (
            f"Step 1: Find LCM({b}, {d}) = {common_lcm}.\n"
            f"Step 2: Express with common denominator:\n"
            f"  {a}/{b} = {a * (common_lcm // b)}/{common_lcm}\n"
            f"  {c}/{d} = {c * (common_lcm // d)}/{common_lcm}\n"
            f"Step 3: Subtract numerators: {a * (common_lcm // b)} - {c * (common_lcm // d)} = {ans.numerator * (common_lcm // ans.denominator)}.\n"
            f"Step 4: Reduce to lowest terms: {correct}."
        )

    else:  # mixed_numbers_borrowing
        # Ensure fractional part of first is smaller than second (requires borrowing)
        b = random.choice([3, 4, 5])
        d = random.choice([2, 3, 4, 6])
        while b == d:
            d = random.choice([2, 3, 5, 6])

        # Pick a/b < c/d
        if Fraction(1, b) < Fraction(1, d):
            a, c = 1, 1
        else:
            a = 1
            c = d - 1

        if Fraction(a, b) >= Fraction(c, d):
            a = 1
            c = d - 1

        w1 = random.randint(4, 7)
        w2 = random.randint(1, w1 - 2)

        total_ans = (w1 + Fraction(a, b)) - (w2 + Fraction(c, d))
        wh = total_ans.numerator // total_ans.denominator
        rem = total_ans.numerator % total_ans.denominator
        correct = _format_mixed(wh, rem, total_ans.denominator)

        # Trap: subtracting smaller from larger without borrowing: (w1 - w2) + (c/d - a/b)
        no_borrow_frac = Fraction(c, d) - Fraction(a, b)
        no_borrow_opt = _format_mixed(w1 - w2, no_borrow_frac.numerator, no_borrow_frac.denominator)

        # Trap: forgot to decrement w1 after borrowing
        forgot_dec = _format_mixed(wh + 1, rem, total_ans.denominator)

        candidates = [
            (no_borrow_opt, "formula_selection_mistake"),
            (forgot_dec, "conceptual_mistake"),
            (_format_mixed(wh, rem + 1, total_ans.denominator), "arithmetic_mistake"),
            (_format_frac(total_ans.numerator, total_ans.denominator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {w1} {a}/{b} - {w2} {c}/{d} (express as a simplified mixed number)"
        expl = (
            f"Step 1: Notice that {a}/{b} < {c}/{d}, so we must borrow 1 from the whole number {w1}.\n"
            f"Step 2: Rewrite {w1} {a}/{b} as ({w1}-1) + (1 + {a}/{b}) = {w1 - 1} {a + b}/{b}.\n"
            f"Step 3: Convert both fractional parts to common denominator {math.lcm(b, d)} and subtract:\n"
            f"  Whole numbers: {w1 - 1} - {w2} = {wh}.\n"
            f"  Fractions: {a + b}/{b} - {c}/{d} = {Fraction(a + b, b) - Fraction(c, d)}.\n"
            f"Step 4: Combined result is {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_subtraction",
        subvariant=variant,
    )

