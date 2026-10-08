import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

def reverse_percentage(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "original_price_after_discount",
        "original_salary_after_raise",
        "price_before_sales_tax",
        "original_population_before_change",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "original_price_after_discount":
        d = random.choice([10, 15, 20, 25, 30, 40, 50])
        orig = random.choice([80, 100, 120, 150, 160, 200, 240, 300])
        s = round(orig * (1 - d / 100), 2)
        if s == int(s):
            s = int(s)
        correct = fmt_curr(orig)
        trap_add_d = fmt_curr(round(s * (1 + d / 100), 2))
        q_text = f"After a {d}% discount, a winter coat sells for ${s}. What was the original price?"
        explanation = (
            f"Step 1: Set up the relationship: Original * (1 - {d}/100) = ${s}.\n"
            f"Step 2: Original * {round(1 - d/100, 2)} = ${s} -> Original = ${s} / {round(1 - d/100, 2)} = {correct}.\n"
            f"GMAT Trap Warning: Do NOT add {d}% of ${s} ({trap_add_d})! The discount was taken on the original price, not the discounted price."
        )
        distractors = [
            (trap_add_d, "percentage_base_mistake"),
            (fmt_curr(round(s / (1 + d / 100), 2)), "conceptual_mistake"),
            (fmt_curr(orig + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, orig - 10)), "arithmetic_mistake"),
        ]

    elif variant == "original_salary_after_raise":
        r = random.choice([10, 12, 15, 20, 25, 30])
        orig = random.choice([40000, 50000, 60000, 75000, 80000])
        s = int(round(orig * (1 + r / 100)))
        correct = fmt_curr(orig)
        trap_sub_r = fmt_curr(round(s * (1 - r / 100)))
        q_text = f"After receiving a {r}% raise, Mia's new salary is ${s:,}. What was her salary before the raise?"
        explanation = (
            f"Step 1: Current Salary = Original * (1 + {r}/100) = Original * {1 + r/100}.\n"
            f"Step 2: Original = ${s:,} / {1 + r/100} = {correct}.\n"
            f"GMAT Trap Warning: Calculating ${s:,} * (1 - {r}/100) gives {trap_sub_r}, which incorrectly discounts the new higher salary!"
        )
        distractors = [
            (trap_sub_r, "percentage_base_mistake"),
            (fmt_curr(round(s / (1 - r / 100))), "conceptual_mistake"),
            (fmt_curr(orig + 2500), "arithmetic_mistake"),
            (fmt_curr(orig - 2500), "arithmetic_mistake"),
        ]

    elif variant == "price_before_sales_tax":
        t = random.choice([5, 8, 10, 12, 15, 20])
        orig = random.choice([100, 150, 200, 250, 300, 400, 500])
        p = round(orig * (1 + t / 100), 2)
        if p == int(p):
            p = int(p)
        correct = fmt_curr(orig)
        trap_sub_t = fmt_curr(round(p * (1 - t / 100), 2))
        q_text = f"The price of a monitor including a {t}% sales tax is ${p}. What was the pre-tax price?"
        explanation = (
            f"Step 1: Pre-Tax Price * (1 + {t}/100) = Total Price (${p}).\n"
            f"Step 2: Pre-Tax Price = ${p} / {1 + t/100} = {correct}."
        )
        distractors = [
            (trap_sub_t, "percentage_base_mistake"),
            (fmt_curr(round(p / (1 - t / 100), 2)), "conceptual_mistake"),
            (fmt_curr(orig + 15), "arithmetic_mistake"),
            (fmt_curr(max(1, orig - 15)), "arithmetic_mistake"),
        ]

    else:  # original_population_before_change
        r = random.choice([10, 20, 25, 30])
        orig = random.choice([5000, 8000, 10000, 12000, 15000, 20000])
        n = int(orig * (1 - r / 100))
        correct = fmt_num(orig)
        trap_add_r = fmt_num(round(n * (1 + r / 100)))
        q_text = f"Following an economic shift, a town's population decreased by {r}% to {n:,}. What was the initial population?"
        explanation = (
            f"Step 1: Initial Population * (1 - {r}/100) = {n:,}.\n"
            f"Step 2: Initial Population = {n:,} / {round(1 - r/100, 2)} = {correct}."
        )
        distractors = [
            (trap_add_r, "percentage_base_mistake"),
            (fmt_num(round(n / (1 + r / 100))), "conceptual_mistake"),
            (fmt_num(orig + 1000), "arithmetic_mistake"),
            (fmt_num(max(100, orig - 1000)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="reverse_percentage",
        subvariant=variant,
    )

