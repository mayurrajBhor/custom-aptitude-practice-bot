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

def generate_decimal_to_fraction(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["terminating_one_place", "terminating_two_places", "terminating_three_places", "mixed_decimal"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "terminating_one_place":
        dec_val = random.choice([0.2, 0.4, 0.6, 0.8])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(dec_val * 10)}/10", "conceptual_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"1/{int(dec_val * 10)}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the terminating decimal {dec_val} into a simplified fraction."
        expl = (
            f"Step 1: Write {dec_val} over 10: {int(dec_val * 10)}/10.\n"
            f"Step 2: Simplify by dividing numerator and denominator by 2: {correct}."
        )

    elif variant == "terminating_two_places":
        dec_val = random.choice([0.15, 0.25, 0.35, 0.45, 0.65, 0.75, 0.85, 0.64])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(round(dec_val * 100))}/100", "conceptual_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"{frac.numerator}/{frac.denominator + 5}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a fraction in lowest terms."
        expl = (
            f"Step 1: Express as a fraction over 100: {int(round(dec_val * 100))}/100.\n"
            f"Step 2: Divide both terms by their GCD ({math.gcd(int(round(dec_val * 100)), 100)}):\n"
            f"  {int(round(dec_val * 100))}/100 = {correct}."
        )

    elif variant == "terminating_three_places":
        dec_val = random.choice([0.125, 0.375, 0.625, 0.875, 0.048, 0.064])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(round(dec_val * 1000))}/1000", "conceptual_mistake"),
            (f"{frac.numerator}/{frac.denominator * 2}", "formula_selection_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a simplified fraction."
        expl = (
            f"Step 1: Write as a fraction over 1,000: {int(round(dec_val * 1000))}/1000.\n"
            f"Step 2: Reduce by dividing by the GCD: {correct}."
        )

    else:  # mixed_decimal
        dec_val = random.choice([1.25, 1.75, 2.5, 3.2, 2.125])
        frac = Fraction(str(dec_val))
        wh = frac.numerator // frac.denominator
        rem = frac.numerator % frac.denominator
        correct = _format_mixed(wh, rem, frac.denominator)

        candidates = [
            (_format_frac(frac.numerator, frac.denominator), "careless_mistake"),
            (_format_mixed(wh + 1, rem, frac.denominator), "arithmetic_mistake"),
            (_format_mixed(wh, rem + 1, frac.denominator), "arithmetic_mistake"),
            (_format_mixed(wh, int((dec_val - wh) * 100), 100), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {dec_val} into a mixed number in simplest form."
        expl = (
            f"Step 1: The whole number part is {wh}.\n"
            f"Step 2: The decimal part is {round(dec_val - wh, 3)} = {rem}/{frac.denominator} in lowest terms.\n"
            f"Step 3: Combine to get the mixed number: {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_to_fraction",
        subvariant=variant,
    )

