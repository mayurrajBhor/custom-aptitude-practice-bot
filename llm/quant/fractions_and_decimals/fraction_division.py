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

def generate_fraction_division(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["keep_change_flip", "whole_and_fraction", "mixed_numbers_division"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "keep_change_flip":
        a = random.randint(2, 5)
        b = random.randint(a + 1, 9)
        c = random.randint(2, 5)
        d = random.randint(c + 1, 9)
        while a * d == b * c:
            d += 1

        ans = Fraction(a * d, b * c)
        correct = _format_frac(ans.numerator, ans.denominator)

        mult_direct = Fraction(a * c, b * d)
        flip_first = Fraction(b * c, a * d)
        flip_both = Fraction(b * d, a * c)

        candidates = [
            (_format_frac(mult_direct.numerator, mult_direct.denominator), "formula_selection_mistake"),
            (_format_frac(flip_first.numerator, flip_first.denominator), "formula_selection_mistake"),
            (_format_frac(flip_both.numerator, flip_both.denominator), "conceptual_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: ({a}/{b}) ÷ ({c}/{d})"
        expl = (
            f"To divide by a fraction, use the 'Keep-Change-Flip' rule:\n"
            f"1. KEEP the first fraction: {a}/{b}\n"
            f"2. CHANGE division (÷) to multiplication (×)\n"
            f"3. FLIP the divisor to its reciprocal: {d}/{c}\n"
            f"Now multiply: ({a}/{b}) × ({d}/{c}) = ({a} × {d}) / ({b} × {c}) = {a * d}/{b * c}.\n"
            f"Simplified: {correct}."
        )

    elif variant == "whole_and_fraction":
        divide_whole_by_frac = random.choice([True, False])
        if divide_whole_by_frac:
            k = random.randint(3, 8)
            b = random.randint(3, 6)
            a = random.randint(1, b - 1)
            ans = Fraction(k * b, a)
            correct = _format_frac(ans.numerator, ans.denominator)
            q_text = f"Calculate: {k} ÷ ({a}/{b})"
            candidates = [
                (_format_frac(k * a, b), "formula_selection_mistake"),
                (_format_frac(a, k * b), "conceptual_mistake"),
                (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
                (str(k * b), "careless_mistake"),
            ]
            expl = (
                f"Step 1: Write {k} as {k}/1.\n"
                f"Step 2: Flip the second fraction to {b}/{a} and multiply: ({k}/1) × ({b}/{a}) = {k * b}/{a}.\n"
                f"Step 3: Simplify: {correct}."
            )
        else:
            b = random.randint(3, 7)
            a = random.randint(1, b - 1)
            k = random.randint(2, 6)
            ans = Fraction(a, b * k)
            correct = _format_frac(ans.numerator, ans.denominator)
            q_text = f"Calculate: ({a}/{b}) ÷ {k}"
            candidates = [
                (_format_frac(a * k, b), "formula_selection_mistake"),
                (_format_frac(b * k, a), "conceptual_mistake"),
                (_format_frac(ans.numerator, ans.denominator + 1), "arithmetic_mistake"),
            ]
            expl = (
                f"Step 1: The reciprocal of integer {k} is 1/{k}.\n"
                f"Step 2: Multiply ({a}/{b}) × (1/{k}) = {a}/{b * k}.\n"
                f"Step 3: Simplify: {correct}."
            )
        distractors, trap_map = _clean_distractors(correct, candidates)

    else:  # mixed_numbers_division
        w1 = random.randint(2, 4)
        w2 = random.randint(1, 2)
        f1 = w1 + Fraction(1, 2)
        f2 = w2 + Fraction(1, 4)
        ans = f1 / f2
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (str(w1 // w2), "conceptual_mistake"),
            (_format_frac((f1 * f2).numerator, (f1 * f2).denominator), "formula_selection_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(ans.denominator, ans.numerator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: ({w1} 1/2) ÷ ({w2} 1/4)"
        expl = (
            f"Step 1: Convert both mixed numbers into improper fractions:\n"
            f"  {w1} 1/2 = {f1.numerator}/{f1.denominator}\n"
            f"  {w2} 1/4 = {f2.numerator}/{f2.denominator}\n"
            f"Step 2: Multiply by the reciprocal of the second fraction:\n"
            f"  ({f1.numerator}/{f1.denominator}) × ({f2.denominator}/{f2.numerator}) = {f1.numerator * f2.denominator}/{f1.denominator * f2.numerator}\n"
            f"Step 3: Simplify to lowest terms: {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_division",
        subvariant=variant,
    )

