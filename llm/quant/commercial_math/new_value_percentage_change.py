import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

def new_value_percentage_change(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "new_value_after_increase",
        "new_value_after_decrease",
        "benchmark_multiplier",
        "multi_step_or_decimal_change",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "new_value_after_increase":
        x = random.choice([50, 80, 120, 150, 200, 350, 500])
        r = random.choice([10, 15, 20, 25, 30, 40, 50])
        ans = round(x * (1 + r / 100), 2)
        if ans == int(ans):
            ans = int(ans)
        correct = fmt_curr(ans)
        q_text = f"An asset originally worth ${x} increased in value by {r}%. What is its new value?"
        explanation = (
            f"Step 1: Multiplier for an increase of {r}% is (1 + {r}/100) = {1 + r/100}.\n"
            f"Step 2: Multiply original value by the multiplier: ${x} * {1 + r/100} = {correct}.\n"
            f"Trap: Do not simply add {r} to ${x} to get ${x + r}!"
        )
        distractors = [
            (fmt_curr(x + r), "percentage_base_mistake"),
            (fmt_curr(round(x * (1 - r / 100), 2)), "conceptual_mistake"),
            (fmt_curr(ans + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, ans - 10)), "arithmetic_mistake"),
        ]

    elif variant == "new_value_after_decrease":
        x = random.choice([60, 80, 100, 120, 160, 200, 300])
        r = random.choice([10, 15, 20, 25, 30, 40, 50])
        ans = round(x * (1 - r / 100), 2)
        if ans == int(ans):
            ans = int(ans)
        correct = fmt_num(ans)
        q_text = f"A company with {x} employees reduced its workforce by {r}%. How many employees remain?"
        explanation = (
            f"Step 1: Multiplier for a decrease of {r}% is (1 - {r}/100) = {round(1 - r/100, 2)}.\n"
            f"Step 2: Multiply: {x} * {round(1 - r/100, 2)} = {correct} employees."
        )
        distractors = [
            (fmt_num(x - r), "percentage_base_mistake"),
            (fmt_num(round(x * (1 + r / 100), 2)), "conceptual_mistake"),
            (fmt_num(ans + 5), "arithmetic_mistake"),
            (fmt_num(max(1, ans - 5)), "arithmetic_mistake"),
        ]

    elif variant == "benchmark_multiplier":
        benchmarks = [
            ("increased", 12.5, 8, 9, "9/8"),
            ("decreased", 12.5, 8, 7, "7/8"),
            ("increased", 25.0, 4, 5, "5/4"),
            ("decreased", 25.0, 4, 3, "3/4"),
            ("increased", 37.5, 8, 11, "11/8"),
            ("decreased", 37.5, 8, 5, "5/8"),
            ("increased", 33.33, 3, 4, "4/3"),
            ("decreased", 33.33, 3, 2, "2/3"),
        ]
        direction, pct, denom, num_mult, frac_str = random.choice(benchmarks)
        k = random.choice([10, 15, 20, 25, 30, 40])
        x = denom * k
        ans = num_mult * k
        correct = fmt_num(ans)
        q_text = f"A quantity of {x} is {direction} by {fmt_pct(pct)}. What is the new value?"
        explanation = (
            f"Step 1: Recognize the benchmark fraction: {fmt_pct(pct)} corresponds to {frac_str}.\n"
            f"Step 2: Apply the multiplier directly: {x} * ({frac_str}) = {correct}."
        )
        opp_ans = (2 * denom - num_mult) * k
        distractors = [
            (fmt_num(round(x + (pct if direction == 'increased' else -pct), 2)), "percentage_base_mistake"),
            (fmt_num(opp_ans), "conceptual_mistake"),
            (fmt_num(ans + 5), "arithmetic_mistake"),
            (fmt_num(max(1, ans - 5)), "arithmetic_mistake"),
        ]

    else:  # multi_step_or_decimal_change
        x = random.choice([200, 400, 600, 800, 1000])
        r = random.choice([4.5, 6.5, 7.5, 8.5, 12.5])
        ans = round(x * (1 + r / 100), 2)
        if ans == int(ans):
            ans = int(ans)
        correct = fmt_curr(ans)
        q_text = f"An initial capital of ${x} grows by {r}%. What is the updated capital amount?"
        explanation = (
            f"Step 1: Multiplier = 1 + ({r}/100) = {1 + r/100}.\n"
            f"Step 2: New Value = ${x} * {1 + r/100} = {correct}."
        )
        distractors = [
            (fmt_curr(x + r), "percentage_base_mistake"),
            (fmt_curr(round(x * (1 - r / 100), 2)), "conceptual_mistake"),
            (fmt_curr(ans + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, ans - 10)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="new_value_percentage_change",
        subvariant=variant,
    )

