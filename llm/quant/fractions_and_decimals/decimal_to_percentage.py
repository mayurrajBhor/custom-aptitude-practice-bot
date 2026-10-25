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

def generate_decimal_to_percentage(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["decimal_to_percent", "percent_to_decimal", "small_and_large_percents"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "decimal_to_percent":
        dec_val = random.choice([0.45, 0.08, 0.375, 0.025, 0.72, 0.05])
        pct_val = dec_val * 100
        correct = f"{pct_val:g}%"

        candidates = [
            (f"{pct_val / 10:g}%", "conceptual_mistake"),
            (f"{pct_val * 10:g}%", "conceptual_mistake"),
            (f"{dec_val:g}%", "formula_selection_mistake"),
            (f"{pct_val + 1:g}%", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a percentage."
        expl = (
            f"To convert a decimal to a percentage, multiply by 100 (shift decimal point 2 places right):\n"
            f"  {dec_val} × 100% = {correct}."
        )

    elif variant == "percent_to_decimal":
        pct_num = random.choice([65, 7.5, 4.25, 125, 8, 3.5])
        dec_val = pct_num / 100
        correct = f"{dec_val:g}"

        candidates = [
            (f"{dec_val * 10:g}", "conceptual_mistake"),
            (f"{dec_val / 10:g}", "conceptual_mistake"),
            (f"{pct_num * 100:g}", "formula_selection_mistake"),
            (f"{dec_val + 0.01:g}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {pct_num}% into a decimal."
        expl = (
            f"To convert a percentage to a decimal, divide by 100 (shift decimal point 2 places left):\n"
            f"  {pct_num}% ÷ 100 = {correct}."
        )

    else:  # small_and_large_percents
        is_small = random.choice([True, False])
        if is_small:
            pct_num = random.choice([0.05, 0.2, 0.08, 0.4])
            dec_val = pct_num / 100
            correct = f"{dec_val:.6g}"
            candidates = [
                (f"{pct_num:.4g}", "conceptual_mistake"),
                (f"{pct_num / 10:.4g}", "conceptual_mistake"),
                (f"{pct_num * 10:.4g}", "formula_selection_mistake"),
            ]
            q_text = f"Convert {pct_num}% into a decimal."
            expl = (
                f"Dividing by 100 shifts the decimal point two places to the left:\n"
                f"  {pct_num}% ÷ 100 = {correct}."
            )
        else:
            pct_num = random.choice([250, 320, 450, 180])
            dec_val = pct_num / 100
            correct = f"{dec_val:g}"
            candidates = [
                (f"{dec_val * 10:g}", "conceptual_mistake"),
                (f"{dec_val / 10:g}", "conceptual_mistake"),
                (f"{pct_num:g}", "careless_mistake"),
            ]
            q_text = f"Convert {pct_num}% into a decimal."
            expl = (
                f"Dividing by 100 shifts the decimal point two places to the left:\n"
                f"  {pct_num}% ÷ 100 = {correct}."
            )
        distractors, trap_map = _clean_distractors(correct, candidates)

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_to_percentage",
        subvariant=variant,
    )

