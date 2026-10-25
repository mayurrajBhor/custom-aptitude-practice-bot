import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

def percentage_vs_percentage_points(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "percentage_points_vs_percent_increase",
        "percentage_points_vs_percent_decrease",
        "interest_rate_change",
        "identify_correct_statement",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "percentage_points_vs_percent_increase":
        p1 = random.choice([20, 25, 40, 50, 60])
        inc_pp = random.choice([5, 10, 15, 20])
        p2 = p1 + inc_pp
        pct_change = round((inc_pp / p1) * 100, 2)
        correct = f"{inc_pp} percentage points, {fmt_pct(pct_change)} increase"
        q_text = (
            f"A politician's approval rating increased from {p1}% to {p2}%. "
            f"By how many percentage points did approval increase, and what was the percentage increase?"
        )
        explanation = (
            f"Step 1: Percentage Points difference = New% - Old% = {p2}% - {p1}% = {inc_pp} percentage points.\n"
            f"Step 2: Percentage Increase = (Difference / Old Base) * 100% = ({inc_pp} / {p1}) * 100% = {fmt_pct(pct_change)}.\n"
            f"Conclusion: An increase of {inc_pp} percentage points represents a {fmt_pct(pct_change)} relative increase."
        )
        distractors = [
            (f"{fmt_pct(pct_change)} percentage points, {inc_pp}% increase", "conceptual_mistake"),
            (f"{inc_pp} percentage points, {fmt_pct(round((inc_pp / p2) * 100, 2))} increase", "percentage_base_mistake"),
            (f"{inc_pp} percentage points, {inc_pp}% increase", "conceptual_mistake"),
            (f"{inc_pp + 2} percentage points, {fmt_pct(pct_change + 5)} increase", "arithmetic_mistake"),
        ]

    elif variant == "percentage_points_vs_percent_decrease":
        p1 = random.choice([40, 50, 60, 80])
        dec_pp = random.choice([10, 15, 20])
        p2 = p1 - dec_pp
        pct_change = round((dec_pp / p1) * 100, 2)
        correct = fmt_pct(pct_change)
        q_text = (
            f"A company's market share decreased from {p1}% to {p2}%. "
            f"What was the percentage decrease in the company's market share?"
        )
        explanation = (
            f"Step 1: Absolute drop in market share rate = {p1}% - {p2}% = {dec_pp} percentage points.\n"
            f"Step 2: Percentage decrease = (Drop / Original Rate) * 100% = ({dec_pp} / {p1}) * 100% = {correct}.\n"
            f"Trap: Do not answer {dec_pp}%, which confuses percentage points with percentage decrease!"
        )
        distractors = [
            (f"{dec_pp}%", "conceptual_mistake"),
            (fmt_pct(round((dec_pp / p2) * 100, 2)), "percentage_base_mistake"),
            (fmt_pct(pct_change + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, pct_change - 5)), "arithmetic_mistake"),
        ]

    elif variant == "interest_rate_change":
        r1 = random.choice([4.0, 5.0, 6.0, 8.0])
        r2 = r1 + random.choice([1.0, 1.5, 2.0])
        pp_diff = round(r2 - r1, 2)
        pct_inc = round((pp_diff / r1) * 100, 2)
        correct = fmt_pct(pct_inc)
        q_text = (
            f"A central bank raised its benchmark interest rate from {fmt_pct(r1)} to {fmt_pct(r2)}. "
            f"What was the percentage increase in the interest rate?"
        )
        explanation = (
            f"Step 1: Increase in rate = {fmt_pct(r2)} - {fmt_pct(r1)} = {pp_diff} percentage points.\n"
            f"Step 2: Percentage Increase in rate = ({pp_diff} / {r1}) * 100% = {correct}."
        )
        distractors = [
            (fmt_pct(pp_diff), "conceptual_mistake"),
            (fmt_pct(round((pp_diff / r2) * 100, 2)), "percentage_base_mistake"),
            (fmt_pct(pct_inc + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, pct_inc - 5)), "arithmetic_mistake"),
        ]

    else:  # identify_correct_statement
        p1 = 10
        p2 = 8
        pp_diff = 2
        pct_drop = 20.0
        correct = f"A decrease of {pp_diff} percentage points, representing a {fmt_pct(pct_drop)} decrease"
        q_text = (
            f"In a certain metropolitan area, the unemployment rate fell from {p1}% to {p2}%. "
            f"Which of the following statements accurately characterizes this change?"
        )
        explanation = (
            f"Step 1: The rate fell by {p1} - {p2} = {pp_diff} percentage points.\n"
            f"Step 2: Relative to the starting rate of {p1}%, this represents a ({pp_diff} / {p1}) * 100% = {fmt_pct(pct_drop)} decrease."
        )
        distractors = [
            (f"A decrease of {fmt_pct(pct_drop)} percentage points, representing a {pp_diff}% decrease", "conceptual_mistake"),
            (f"A decrease of {pp_diff} percentage points, representing a {fmt_pct(round(pp_diff/p2*100, 2))} decrease", "percentage_base_mistake"),
            (f"A decrease of {pp_diff}%, with 0 percentage points change", "conceptual_mistake"),
            (f"A decrease of 4 percentage points, representing a 40% decrease", "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="percentage_vs_percentage_points",
        subvariant=variant,
    )

