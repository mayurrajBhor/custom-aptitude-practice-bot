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

def generate_fraction_multiplication(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["direct_multiplication", "cross_cancellation", "whole_times_fraction", "multiple_fractions"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "direct_multiplication":
        a = random.randint(1, 5)
        b = random.randint(a + 1, 7)
        c = random.randint(1, 5)
        d = random.randint(c + 1, 8)
        ans = Fraction(a * c, b * d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a * d, b * c), "formula_selection_mistake"),
            (_format_frac(a + c, b + d), "conceptual_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(b * d, a * c), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Multiply: {a}/{b} × {c}/{d}"
        expl = (
            f"Step 1: Multiply numerators straight across: {a} × {c} = {a * c}.\n"
            f"Step 2: Multiply denominators straight across: {b} × {d} = {b * d}.\n"
            f"Step 3: Reduce the resulting fraction: {a * c}/{b * d} = {correct}.\n"
            f"Trap: Do not cross-multiply ({a}×{d} / {b}×{c}) when multiplying fractions."
        )

    elif variant == "cross_cancellation":
        # Fraction 1: a/b, Fraction 2: (k*b)/c, so b cancels
        b = random.choice([3, 4, 5, 7])
        k = random.choice([2, 3])
        a = random.randint(1, b - 1)
        c = random.randint(k * a + 1, max(k * a + 5, 20))
        while math.gcd(k * a, c) == c:
            c += 1

        f1 = f"{a}/{b}"
        f2 = f"{k * b}/{c}"
        ans = Fraction(a * k * b, b * c)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a * k * b, c), "conceptual_mistake"),
            (_format_frac(ans.denominator, ans.numerator), "careless_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(a * c, b * k * b), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Compute using cross-cancellation: {f1} × {f2}"
        expl = (
            f"Step 1: Look for common factors between numerators and denominators.\n"
            f"Notice that {b} in the denominator of the first fraction and {k * b} in the numerator of the second "
            f"both divide by {b}: {k * b} ÷ {b} = {k} and {b} ÷ {b} = 1.\n"
            f"Step 2: Multiply the simplified terms: ({a} × {k}) / (1 × {c}) = {a * k}/{c}.\n"
            f"Step 3: Reduce to lowest terms: {correct}."
        )

    elif variant == "whole_times_fraction":
        k = random.randint(3, 8)
        b = random.randint(3, 7)
        a = random.randint(1, b - 1)
        ans = Fraction(k * a, b)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a, b), "conceptual_mistake"),
            (_format_frac(a, k * b), "formula_selection_mistake"),
            (_format_frac(k * a + 1, b), "arithmetic_mistake"),
            (_format_frac(k + a, b), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {k} × {a}/{b}"
        expl = (
            f"Step 1: Express the integer {k} as a fraction: {k}/1.\n"
            f"Step 2: Multiply numerators and denominators: ({k} × {a}) / (1 × {b}) = {k * a}/{b}.\n"
            f"Step 3: Simplify: {correct}.\n"
            f"Trap: Do NOT multiply both numerator and denominator by {k} (e.g. {k*a}/{k*b} = {a}/{b})."
        )

    else:  # multiple_fractions
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 3)
        f3 = Fraction(3, 5)
        ans = f1 * f2 * f3
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            ("1/2", "arithmetic_mistake"),
            ("6/30", "conceptual_mistake"),
            ("2/5", "arithmetic_mistake"),
            ("1/3", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Calculate the product: (1/2) × (2/3) × (3/5)"
        expl = (
            f"Step 1: Cancel common factors across numerators and denominators:\n"
            f"  - The 2 in the denominator of (1/2) cancels with the 2 in the numerator of (2/3).\n"
            f"  - The 3 in the denominator of (2/3) cancels with the 3 in the numerator of (3/5).\n"
            f"Step 2: The remaining product is (1 × 1 × 1) / (1 × 1 × 5) = 1/5."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_multiplication",
        subvariant=variant,
    )

