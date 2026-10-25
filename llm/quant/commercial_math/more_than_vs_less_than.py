import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

def more_than_vs_less_than(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "a_more_than_b_direct",
        "b_less_than_a_direct",
        "a_is_x_percent_more_then_b_is_what_less",
        "a_is_x_percent_less_then_b_is_what_more",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "a_more_than_b_direct":
        y = random.choice([50, 80, 100, 120, 160, 200])
        p = random.choice([20, 25, 40, 50, 60, 75, 100])
        x = int(round(y * (1 + p / 100)))
        diff = x - y
        correct = fmt_pct(p)
        trap_divided_by_x = fmt_pct(round((diff / x) * 100, 2))
        q_text = (
            f"Company A has {x} employees and Company B has {y} employees. "
            f"The number of employees in Company A is what percent more than the number of employees in Company B?"
        )
        explanation = (
            f"Step 1: 'More than B' means B is the denominator anchor base!\n"
            f"Step 2: Difference = A - B = {x} - {y} = {diff}.\n"
            f"Step 3: % More = (Difference / B) * 100% = ({diff} / {y}) * 100% = {correct}.\n"
            f"Trap Warning: Dividing by A ({x}) yields {trap_divided_by_x}, which answers 'B is what % less than A'."
        )
        distractors = [
            (trap_divided_by_x, "percentage_base_mistake"),
            (fmt_num(diff), "careless_mistake"),
            (fmt_pct(p + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, p - 5)), "arithmetic_mistake"),
        ]

    elif variant == "b_less_than_a_direct":
        y = random.choice([50, 80, 100, 120, 160, 200])
        p = random.choice([20, 25, 40, 50, 60, 75, 100])
        x = int(round(y * (1 + p / 100)))
        diff = x - y
        pct_less = round((diff / x) * 100, 2)
        correct = fmt_pct(pct_less)
        trap_divided_by_y = fmt_pct(round((diff / y) * 100, 2))
        q_text = (
            f"Company A has {x} employees and Company B has {y} employees. "
            f"The number of employees in Company B is what percent less than the number of employees in Company A?"
        )
        explanation = (
            f"Step 1: 'Less than A' means A is the denominator anchor base!\n"
            f"Step 2: Difference = {x} - {y} = {diff}.\n"
            f"Step 3: % Less = (Difference / A) * 100% = ({diff} / {x}) * 100% = {correct}."
        )
        distractors = [
            (trap_divided_by_y, "percentage_base_mistake"),
            (fmt_num(diff), "careless_mistake"),
            (fmt_pct(pct_less + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, pct_less - 5)), "arithmetic_mistake"),
        ]

    elif variant == "a_is_x_percent_more_then_b_is_what_less":
        pairs = [
            (25, 20.0),
            (50, 33.33),
            (100, 50.0),
            (20, 16.67),
            (33.33, 25.0),
        ]
        x_pct, ans_pct = random.choice(pairs)
        correct = fmt_pct(ans_pct)
        q_text = (
            f"If quantity A is {fmt_pct(x_pct)} more than quantity B, "
            f"then quantity B is what percent less than quantity A?"
        )
        explanation = (
            f"Step 1: Let quantity B = 100. Then quantity A = 100 + {x_pct} = {100 + x_pct}.\n"
            f"Step 2: Difference = {x_pct}.\n"
            f"Step 3: Percentage B is less than A = (Difference / A) * 100% = ({x_pct} / {100 + x_pct}) * 100% = {correct}.\n"
            f"GMAT Trap: Never say {fmt_pct(x_pct)}! Because A is larger than B, the same difference represents a smaller percentage of A."
        )
        distractors = [
            (fmt_pct(x_pct), "percentage_base_mistake"),
            (fmt_pct(round((x_pct / (100 - x_pct)) * 100, 2)) if x_pct < 100 else "75%", "conceptual_mistake"),
            (fmt_pct(ans_pct + 4), "arithmetic_mistake"),
            (fmt_pct(max(1.0, ans_pct - 4)), "arithmetic_mistake"),
        ]

    else:  # a_is_x_percent_less_then_b_is_what_more
        pairs = [
            (20, 25.0),
            (25, 33.33),
            (50, 100.0),
            (10, 11.11),
            (16.67, 20.0),
        ]
        x_pct, ans_pct = random.choice(pairs)
        correct = fmt_pct(ans_pct)
        q_text = (
            f"If quantity A is {fmt_pct(x_pct)} less than quantity B, "
            f"then quantity B is what percent more than quantity A?"
        )
        explanation = (
            f"Step 1: Let B = 100. Then A = 100 - {x_pct} = {100 - x_pct}.\n"
            f"Step 2: Difference = {x_pct}.\n"
            f"Step 3: % More = (Difference / A) * 100% = ({x_pct} / {100 - x_pct}) * 100% = {correct}."
        )
        distractors = [
            (fmt_pct(x_pct), "percentage_base_mistake"),
            (fmt_pct(round((x_pct / (100 + x_pct)) * 100, 2)), "conceptual_mistake"),
            (fmt_pct(ans_pct + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, ans_pct - 5)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="more_than_vs_less_than",
        subvariant=variant,
    )

