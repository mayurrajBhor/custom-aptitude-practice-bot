"""Day 3 of GMAT Practice Engine: Percentages & Commercial Math (Patterns 5025 - 5039).

Covers core concepts:
- Fundamentals, increases, decreases, multipliers, reverse percentages
- Successive changes and symmetric traps
- Profit, loss, markups, discounts, combined schemes, successive discounts
- Percentage vs Percentage Points trap distinctions
- More Than vs Less Than base shifting
- Multi-step realistic GMAT word problems
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.gmat.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq


# -------------------------------------------------------------------------
# Formatting Utilities
# -------------------------------------------------------------------------
def fmt_pct(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"{int(round(val))}%"
    return f"{val:.2f}%"


def fmt_curr(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"${int(round(val))}"
    return f"${val:.2f}"


def fmt_num(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"{int(round(val))}"
    return f"{val:.2f}"


def build_mcq(
    question: str,
    correct: Any,
    explanation: str,
    difficulty: int,
    raw_distractors: List[Tuple[Any, str]],
    pattern_name: str,
    subvariant: str,
) -> Dict[str, Any]:
    correct_str = str(correct).strip()
    distractor_list: List[str] = []
    trap_map: Dict[str, str] = {}

    for val, trap_type in raw_distractors:
        d_str = str(val).strip()
        if d_str and d_str != correct_str and d_str not in distractor_list:
            distractor_list.append(d_str)
            trap_map[d_str] = trap_type

    return make_mcq(
        question=question,
        correct=correct_str,
        explanation=explanation,
        difficulty=difficulty,
        distractors=distractor_list,
        trap_map=trap_map,
        pattern_name=pattern_name,
        subvariant=subvariant,
    )


# =========================================================================
# Pattern 5025: percentage_fundamentals
# =========================================================================
def percentage_fundamentals(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_percentage_of_number",
        "what_percentage_is_a_of_b",
        "find_base_from_percentage",
        "fraction_to_percentage",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "find_percentage_of_number":
        if level == 1:
            p = random.choice([10, 20, 25, 50])
            n = random.choice([40, 60, 80, 100, 120, 160, 200])
            ans = (p * n) // 100
        elif level == 2:
            p = random.choice([15, 30, 40, 60, 75])
            n = random.choice([60, 80, 120, 140, 180, 240, 300])
            ans = (p * n) // 100
        elif level == 3:
            p = random.choice([12, 18, 35, 45, 65, 85])
            n = random.choice([150, 250, 350, 450, 550, 650])
            ans = round((p * n) / 100, 2)
        elif level == 4:
            benchmark = random.choice([
                (12.5, 8, "12.5%"),
                (37.5, 8, "37.5%"),
                (62.5, 8, "62.5%"),
                (87.5, 8, "87.5%"),
                (16.67, 6, "16.67%"),
                (33.33, 3, "33.33%"),
            ])
            p_val, denom, p_str = benchmark
            k = random.choice([20, 30, 40, 50, 60])
            n = denom * k
            p = p_val
            ans = int(round((p_val * n) / 100))
        else:
            benchmark = random.choice([
                (14.28, 7, "14.28%"),
                (8.33, 12, "8.33%"),
                (66.67, 3, "66.67%"),
                (83.33, 6, "83.33%"),
            ])
            p_val, denom, p_str = benchmark
            k = random.choice([35, 42, 49, 70])
            n = denom * k
            p = p_val
            ans = int(round((p_val * n) / 100))

        correct = fmt_num(ans)
        q_text = f"What is {fmt_pct(p)} of {n}?"
        explanation = (
            f"Step 1: Convert the percentage into a multiplier: {fmt_pct(p)} = {p}/100 = {round(p/100, 4)}.\n"
            f"Step 2: Multiply by {n}: {p}/100 * {n} = {correct}.\n"
            f"Conclusion: {fmt_pct(p)} of {n} is {correct}."
        )
        distractors = [
            (fmt_num(round((p * n) / 10, 2)), "percentage_base_mistake"),
            (fmt_num(ans + (5 if ans > 10 else 2)), "arithmetic_mistake"),
            (fmt_num(ans - (5 if ans > 15 else 1)), "arithmetic_mistake"),
            (fmt_num(round(((100 - p) * n) / 100, 2)), "careless_mistake"),
        ]

    elif variant == "what_percentage_is_a_of_b":
        if level <= 2:
            b = random.choice([50, 100, 150, 200, 250, 400])
            p = random.choice([10, 20, 25, 30, 40, 50, 60, 75])
        elif level <= 4:
            b = random.choice([80, 120, 160, 240, 320, 480])
            p = random.choice([12.5, 15, 35, 37.5, 45, 62.5, 75])
        else:
            b = random.choice([140, 210, 280, 350, 420])
            p = random.choice([14.28, 16.67, 33.33, 66.67, 83.33])

        a = round((p * b) / 100, 2)
        if a == int(a):
            a = int(a)

        correct = fmt_pct(p)
        q_text = f"{a} is what percent of {b}?"
        inv_pct = round((b / a) * 100, 2) if a != 0 else 0
        diff_pct = round(((b - a) / b) * 100, 2)

        explanation = (
            f"Step 1: Identify Part and Base: Part = {a}, Base (Whole) = {b}.\n"
            f"Step 2: Set up the percentage formula: (Part / Base) * 100% = ({a} / {b}) * 100%.\n"
            f"Step 3: Calculate: {a}/{b} = {round(a/b, 4)} -> {correct}.\n"
            f"Watch out for the base trap: dividing {b} by {a} gives {fmt_pct(inv_pct)}, which is inverted!"
        )
        distractors = [
            (fmt_pct(inv_pct), "percentage_base_mistake"),
            (fmt_pct(diff_pct), "careless_mistake"),
            (fmt_pct(p + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, p - 5)), "arithmetic_mistake"),
        ]

    elif variant == "find_base_from_percentage":
        if level <= 2:
            p = random.choice([10, 20, 25, 50])
            n = random.choice([50, 80, 100, 150, 200, 300])
        elif level <= 4:
            p = random.choice([12, 15, 30, 35, 40, 60, 75])
            n = random.choice([120, 240, 360, 400, 500, 800])
        else:
            p = random.choice([16, 24, 32, 48, 64, 80])
            n = random.choice([350, 450, 625, 750, 850])

        a = (p * n) // 100 if (p * n) % 100 == 0 else round((p * n) / 100, 2)
        correct = fmt_num(n)
        q_text = f"If {fmt_pct(p)} of a number N is {a}, what is the value of N?"
        explanation = (
            f"Step 1: Translate the word equation: ({p}/100) * N = {a}.\n"
            f"Step 2: Isolate N by dividing {a} by {p}/100: N = {a} / ({p}/100) = {a} * (100/{p}).\n"
            f"Step 3: Calculate: N = {correct}."
        )
        distractors = [
            (fmt_num(round(a * (p / 100), 2)), "percentage_base_mistake"),
            (fmt_num(round(a * p, 2)), "conceptual_mistake"),
            (fmt_num(n + (20 if n >= 100 else 5)), "arithmetic_mistake"),
            (fmt_num(max(5, n - (20 if n >= 100 else 5))), "arithmetic_mistake"),
        ]

    else:  # fraction_to_percentage
        fractions_pool = [
            (1, 2, 50.0),
            (1, 4, 25.0),
            (3, 4, 75.0),
            (1, 5, 20.0),
            (2, 5, 40.0),
            (3, 5, 60.0),
            (4, 5, 80.0),
            (1, 8, 12.5),
            (3, 8, 37.5),
            (5, 8, 62.5),
            (7, 8, 87.5),
            (1, 6, 16.67),
            (5, 6, 83.33),
            (1, 3, 33.33),
            (2, 3, 66.67),
        ]
        num, den, pct_val = random.choice(fractions_pool)
        correct = fmt_pct(pct_val)
        q_text = f"Express the fraction {num}/{den} as a percentage."
        inv_pct = round((den / num) * 100, 2)
        compl_pct = round(100 - pct_val, 2)
        explanation = (
            f"Step 1: Multiply the fraction by 100%: ({num}/{den}) * 100%.\n"
            f"Step 2: ({num} * 100) / {den} = {num * 100} / {den} = {correct}."
        )
        distractors = [
            (fmt_pct(inv_pct), "conceptual_mistake"),
            (fmt_pct(compl_pct), "careless_mistake"),
            (fmt_pct(pct_val + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, pct_val - 5)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="percentage_fundamentals",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5026: percentage_increase
# =========================================================================
def percentage_increase(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["price_increase", "population_growth", "salary_hike", "revenue_expansion"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if level <= 2:
        x = random.choice([40, 50, 60, 80, 100, 120, 200])
        p = random.choice([10, 20, 25, 30, 50, 75, 100])
    elif level <= 4:
        x = random.choice([75, 125, 150, 180, 240, 320, 450])
        p = random.choice([12, 15, 35, 40, 60, 80, 125])
    else:
        x = random.choice([160, 220, 340, 480, 560, 640])
        p = random.choice([12.5, 37.5, 62.5, 87.5, 17.5, 45])

    y = round(x * (1 + p / 100), 2)
    if y == int(y):
        y = int(y)
    diff = round(y - x, 2)
    if diff == int(diff):
        diff = int(diff)

    correct = fmt_pct(p)
    trap_new_base = fmt_pct(round((diff / y) * 100, 2))

    if variant == "price_increase":
        q_text = f"The price of a jacket increased from ${x} to ${y}. What is the percentage increase?"
    elif variant == "population_growth":
        q_text = f"The population of a town increased from {x:,} to {y:,}. What was the percentage increase?"
    elif variant == "salary_hike":
        q_text = f"An employee's annual salary increased from ${x:,} to ${y:,}. Find the percentage hike."
    else:  # revenue_expansion
        q_text = f"A firm's quarterly revenue rose from ${x} million to ${y} million. What is the percentage increase?"

    explanation = (
        f"Step 1: Compute absolute increase: New - Original = {y} - {x} = {diff}.\n"
        f"Step 2: Divide by the ORIGINAL base (not the new base!): {diff} / {x} = {round(diff/x, 4)}.\n"
        f"Step 3: Convert to percentage: {round(diff/x, 4)} * 100% = {correct}.\n"
        f"Trap Warning: Dividing by the new value {y} gives {trap_new_base}, which is the classic GMAT base trap!"
    )

    distractors = [
        (trap_new_base, "percentage_base_mistake"),
        (fmt_pct(round((y / x) * 100, 2)), "conceptual_mistake"),
        (f"{diff}%", "careless_mistake"),
        (fmt_pct(p + 5), "arithmetic_mistake"),
    ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="percentage_increase",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5027: percentage_decrease
# =========================================================================
def percentage_decrease(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["price_reduction", "population_decline", "budget_cut", "inventory_depletion"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if level <= 2:
        x = random.choice([50, 80, 100, 120, 150, 200])
        p = random.choice([10, 20, 25, 30, 40, 50])
    elif level <= 4:
        x = random.choice([80, 120, 160, 240, 300, 400])
        p = random.choice([15, 35, 45, 60, 70, 75])
    else:
        x = random.choice([160, 240, 320, 480, 560, 640])
        p = random.choice([12.5, 37.5, 62.5, 17.5, 22.5])

    y = round(x * (1 - p / 100), 2)
    if y == int(y):
        y = int(y)
    diff = round(x - y, 2)
    if diff == int(diff):
        diff = int(diff)

    correct = fmt_pct(p)
    trap_new_base = fmt_pct(round((diff / y) * 100, 2))

    if variant == "price_reduction":
        q_text = f"The price of an appliance dropped from ${x} to ${y}. What is the percentage decrease?"
    elif variant == "population_decline":
        q_text = f"The population of a borough decreased from {x:,} to {y:,}. What was the percentage decrease?"
    elif variant == "budget_cut":
        q_text = f"A department's annual budget was reduced from ${x:,} to ${y:,}. Find the percentage decrease."
    else:  # inventory_depletion
        q_text = f"A store's inventory of smartphones fell from {x} units to {y} units. What is the percentage decrease?"

    explanation = (
        f"Step 1: Compute absolute decrease: Original - New = {x} - {y} = {diff}.\n"
        f"Step 2: Percentage decrease is ALWAYS calculated over the ORIGINAL base ({x}): "
        f"({diff} / {x}) * 100% = {correct}.\n"
        f"Trap Warning: Dividing by the new lower value ({y}) yields {trap_new_base}, which is a percentage base mistake."
    )

    distractors = [
        (trap_new_base, "percentage_base_mistake"),
        (fmt_pct(round((y / x) * 100, 2)), "conceptual_mistake"),
        (f"{diff}%", "careless_mistake"),
        (fmt_pct(p + 5), "arithmetic_mistake"),
    ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="percentage_decrease",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5028: new_value_percentage_change
# =========================================================================
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


# =========================================================================
# Pattern 5029: reverse_percentage
# =========================================================================
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


# =========================================================================
# Pattern 5030: successive_percentage_changes
# =========================================================================
def successive_percentage_changes(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_increases",
        "increase_then_decrease",
        "symmetric_change_trap",
        "three_successive_changes",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "two_increases":
        a = random.choice([10, 15, 20, 25, 30, 40])
        b = random.choice([10, 15, 20, 25, 30])
        net = round(a + b + (a * b) / 100, 2)
        correct = fmt_pct(net)
        q_text = f"A share price increases by {a}% in January and then increases by {b}% in February. What is the overall percentage increase?"
        simple_sum = fmt_pct(a + b)
        explanation = (
            f"Step 1: Chain multipliers: (1 + {a}/100) * (1 + {b}/100) = {1 + a/100} * {1 + b/100} = {round((1+a/100)*(1+b/100), 4)}.\n"
            f"Step 2: Subtract 1: {round((1+a/100)*(1+b/100) - 1, 4)} * 100% = {correct}.\n"
            f"Alternatively, use formula a + b + (a*b)/100 = {a} + {b} + {a*b/100} = {correct}.\n"
            f"Trap Warning: Never just add percentages ({simple_sum})! The second increase applies to a larger base."
        )
        distractors = [
            (simple_sum, "conceptual_mistake"),
            (fmt_pct(round(a + b - (a * b) / 100, 2)), "percentage_base_mistake"),
            (fmt_pct(net + 2), "arithmetic_mistake"),
            (fmt_pct(max(1.0, net - 2)), "arithmetic_mistake"),
        ]

    elif variant == "increase_then_decrease":
        a = random.choice([20, 25, 30, 40, 50])
        b = random.choice([10, 15, 20, 25, 30])
        net = round(((1 + a / 100) * (1 - b / 100) - 1) * 100, 2)
        label = "increase" if net > 0 else "decrease"
        correct = f"{abs(net):.2f}% {label}".replace(".00%", "%")
        q_text = f"The price of an asset increases by {a}% and subsequently decreases by {b}%. What is the net percentage change?"
        simple_diff = a - b
        simple_label = "increase" if simple_diff > 0 else "decrease"
        simple_str = f"{abs(simple_diff)}% {simple_label}"
        opp_label = "decrease" if net > 0 else "increase"
        opp_str = f"{abs(net):.2f}% {opp_label}".replace(".00%", "%")

        explanation = (
            f"Step 1: Chain multipliers: (1 + {a}/100) * (1 - {b}/100) = {1 + a/100} * {round(1 - b/100, 2)} = {round((1+a/100)*(1-b/100), 4)}.\n"
            f"Step 2: Net change = {round((1+a/100)*(1-b/100) - 1, 4)} * 100% = {correct}.\n"
            f"Trap: Simple subtraction yields {simple_str}, which ignores the changed base."
        )
        distractors = [
            (simple_str, "conceptual_mistake"),
            (opp_str, "conceptual_mistake"),
            (f"{abs(net) + 3:.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
            (f"{max(1.0, abs(net) - 3):.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
        ]

    elif variant == "symmetric_change_trap":
        x = random.choice([10, 15, 20, 25, 30, 40, 50])
        loss_pct = round((x * x) / 100, 2)
        correct = f"{loss_pct:.2f}% decrease".replace(".00%", "%")
        q_text = (
            f"The price of a commodity increases by {x}% and then decreases by {x}%. "
            f"What is the net percentage change?"
        )
        explanation = (
            f"Step 1: Multiplier chaining: (1 + {x}/100) * (1 - {x}/100) = 1 - ({x}/100)^2 = 1 - {loss_pct/100}.\n"
            f"Step 2: Net change is ALWAYS a decrease of x^2/100 % = {x}^2 / 100 % = {loss_pct}% decrease.\n"
            f"GMAT Trap: Most test-takers fall for '0% (No change)'. Because the decrease is applied to a larger value, the net result is always a loss!"
        )
        distractors = [
            ("0% (No change)", "conceptual_mistake"),
            (f"{loss_pct:.2f}% increase".replace(".00%", "%"), "percentage_base_mistake"),
            (f"{x}% decrease", "careless_mistake"),
            (f"{round(loss_pct + 1, 2)}% decrease", "arithmetic_mistake"),
        ]

    else:  # three_successive_changes
        a = random.choice([10, 20, 25])
        b = random.choice([10, 20])
        c = random.choice([10, 15, 20])
        mult = (1 + a / 100) * (1 - b / 100) * (1 + c / 100)
        net = round((mult - 1) * 100, 2)
        label = "increase" if net >= 0 else "decrease"
        correct = f"{abs(net):.2f}% {label}".replace(".00%", "%")
        q_text = f"A portfolio value changes consecutively by +{a}%, -{b}%, and +{c}%. What is the overall percentage change?"
        simple_sum = a - b + c
        simple_str = f"{abs(simple_sum)}% {'increase' if simple_sum >= 0 else 'decrease'}"
        explanation = (
            f"Step 1: Multiply all 3 factors: (1 + {a/100}) * (1 - {b/100}) * (1 + {c/100}) = {round(mult, 4)}.\n"
            f"Step 2: Overall change = ({round(mult, 4)} - 1) * 100% = {correct}."
        )
        distractors = [
            (simple_str, "conceptual_mistake"),
            (f"{abs(net):.2f}% {'decrease' if label == 'increase' else 'increase'}".replace(".00%", "%"), "conceptual_mistake"),
            (f"{abs(net) + 2:.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
            (f"{max(1.0, abs(net) - 2):.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="successive_percentage_changes",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5031: profit_and_loss
# =========================================================================
def profit_and_loss(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "calculate_profit_percentage",
        "calculate_loss_percentage",
        "profit_with_overhead",
        "sp_per_unit_vs_cp",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "calculate_profit_percentage":
        cp = random.choice([40, 50, 60, 80, 100, 120, 150, 200])
        p = random.choice([10, 15, 20, 25, 30, 40, 50])
        sp = round(cp * (1 + p / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        profit = sp - cp
        correct = fmt_pct(p)
        trap_sp_base = fmt_pct(round((profit / sp) * 100, 2))
        q_text = f"A merchant purchases an item for ${cp} and sells it for ${sp}. What is the profit percentage?"
        explanation = (
            f"Step 1: Profit amount = SP - CP = ${sp} - ${cp} = ${profit}.\n"
            f"Step 2: Profit % is ALWAYS calculated over Cost Price (CP): (${profit} / ${cp}) * 100% = {correct}.\n"
            f"Trap: Dividing by SP (${sp}) gives {trap_sp_base}, which is profit margin, not profit percentage!"
        )
        distractors = [
            (trap_sp_base, "percentage_base_mistake"),
            (fmt_curr(profit), "careless_mistake"),
            (fmt_pct(p + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, p - 5)), "arithmetic_mistake"),
        ]

    elif variant == "calculate_loss_percentage":
        cp = random.choice([50, 80, 100, 120, 160, 200, 250])
        l = random.choice([10, 15, 20, 25, 30, 40])
        sp = round(cp * (1 - l / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        loss = cp - sp
        correct = fmt_pct(l)
        trap_sp_base = fmt_pct(round((loss / sp) * 100, 2))
        q_text = f"A retailer buys inventory for ${cp} and sells it at a clearance price of ${sp}. What is the loss percentage?"
        explanation = (
            f"Step 1: Loss amount = CP - SP = ${cp} - ${sp} = ${loss}.\n"
            f"Step 2: Loss % is calculated on Cost Price (CP): (${loss} / ${cp}) * 100% = {correct}.\n"
            f"Trap Warning: Dividing by SP (${sp}) gives {trap_sp_base}."
        )
        distractors = [
            (trap_sp_base, "percentage_base_mistake"),
            (fmt_curr(loss), "careless_mistake"),
            (fmt_pct(l + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, l - 5)), "arithmetic_mistake"),
        ]

    elif variant == "profit_with_overhead":
        base_cp = random.choice([150, 200, 300, 400, 500])
        overhead = random.choice([20, 40, 50, 60, 100])
        total_cp = base_cp + overhead
        p = random.choice([10, 15, 20, 25, 30])
        sp = int(round(total_cp * (1 + p / 100)))
        profit = sp - total_cp
        correct = fmt_pct(p)
        trap_ignore_overhead = fmt_pct(round(((sp - base_cp) / base_cp) * 100, 2))
        q_text = (
            f"A trader purchases machinery for ${base_cp} and spends ${overhead} on repairs and transportation. "
            f"If he sells the machine for ${sp}, what is his profit percentage?"
        )
        explanation = (
            f"Step 1: Total CP = Purchase Price + Overheads = ${base_cp} + ${overhead} = ${total_cp}.\n"
            f"Step 2: Profit = SP - Total CP = ${sp} - ${total_cp} = ${profit}.\n"
            f"Step 3: Profit % = (${profit} / ${total_cp}) * 100% = {correct}.\n"
            f"Trap Warning: Forgetting overheads and using base purchase price (${base_cp}) yields {trap_ignore_overhead}."
        )
        distractors = [
            (trap_ignore_overhead, "careless_mistake"),
            (fmt_pct(round((profit / sp) * 100, 2)), "percentage_base_mistake"),
            (fmt_pct(p + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, p - 5)), "arithmetic_mistake"),
        ]

    else:  # sp_per_unit_vs_cp
        n_units = random.choice([10, 12, 15, 20, 25])
        unit_cp = random.choice([8, 10, 12, 15, 20])
        total_cp = n_units * unit_cp
        p = random.choice([20, 25, 30, 50])
        unit_sp = round(unit_cp * (1 + p / 100), 2)
        if unit_sp == int(unit_sp):
            unit_sp = int(unit_sp)
        correct = fmt_pct(p)
        q_text = (
            f"A wholesaler buys {n_units} crates for a total of ${total_cp} and sells them at ${unit_sp} per crate. "
            f"What is the profit percentage on the transaction?"
        )
        total_sp = round(n_units * unit_sp, 2)
        explanation = (
            f"Step 1: Find CP per unit: ${total_cp} / {n_units} = ${unit_cp}.\n"
            f"Step 2: Profit per unit = ${unit_sp} - ${unit_cp} = ${round(unit_sp - unit_cp, 2)}.\n"
            f"Step 3: Profit % = (${round(unit_sp - unit_cp, 2)} / ${unit_cp}) * 100% = {correct}."
        )
        distractors = [
            (fmt_pct(round(((unit_sp - unit_cp) / unit_sp) * 100, 2)), "percentage_base_mistake"),
            (fmt_curr(round(total_sp - total_cp, 2)), "careless_mistake"),
            (fmt_pct(p + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, p - 5)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="profit_and_loss",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5032: profit_loss_multipliers
# =========================================================================
def profit_loss_multipliers(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_sp_from_cp_and_profit",
        "find_sp_from_cp_and_loss",
        "find_cp_from_sp_and_profit",
        "find_cp_from_sp_and_loss",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "find_sp_from_cp_and_profit":
        cp = random.choice([50, 75, 120, 160, 200, 350, 480])
        p = random.choice([10, 15, 20, 25, 30, 40])
        sp = round(cp * (1 + p / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(sp)
        q_text = f"An article costing ${cp} is sold at a {p}% profit. What is the selling price?"
        explanation = (
            f"Step 1: SP multiplier for {p}% profit = (1 + {p}/100) = {1 + p/100}.\n"
            f"Step 2: SP = ${cp} * {1 + p/100} = {correct}."
        )
        distractors = [
            (fmt_curr(round(cp * (1 - p / 100), 2)), "conceptual_mistake"),
            (fmt_curr(cp + p), "percentage_base_mistake"),
            (fmt_curr(sp + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, sp - 10)), "arithmetic_mistake"),
        ]

    elif variant == "find_sp_from_cp_and_loss":
        cp = random.choice([60, 80, 100, 150, 200, 300, 450])
        l = random.choice([10, 15, 20, 25, 30, 40])
        sp = round(cp * (1 - l / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(sp)
        q_text = f"An item with cost price ${cp} is sold at a {l}% loss. What is the selling price?"
        explanation = (
            f"Step 1: SP multiplier for {l}% loss = (1 - {l}/100) = {round(1 - l/100, 2)}.\n"
            f"Step 2: SP = ${cp} * {round(1 - l/100, 2)} = {correct}."
        )
        distractors = [
            (fmt_curr(round(cp * (1 + l / 100), 2)), "conceptual_mistake"),
            (fmt_curr(cp - l), "percentage_base_mistake"),
            (fmt_curr(sp + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, sp - 10)), "arithmetic_mistake"),
        ]

    elif variant == "find_cp_from_sp_and_profit":
        cp = random.choice([50, 80, 100, 120, 160, 200, 250, 400])
        p = random.choice([10, 15, 20, 25, 30, 50])
        sp = round(cp * (1 + p / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(cp)
        trap_sub_p = fmt_curr(round(sp * (1 - p / 100), 2))
        q_text = f"By selling an item for ${sp}, a vendor makes a {p}% profit. What was the cost price?"
        explanation = (
            f"Step 1: Relationship: CP * (1 + {p}/100) = SP (${sp}).\n"
            f"Step 2: CP = ${sp} / {1 + p/100} = {correct}.\n"
            f"Trap: Do not subtract {p}% from SP ({trap_sub_p})! Profit is based on CP, not SP."
        )
        distractors = [
            (trap_sub_p, "percentage_base_mistake"),
            (fmt_curr(round(sp / (1 - p / 100), 2)), "conceptual_mistake"),
            (fmt_curr(cp + 15), "arithmetic_mistake"),
            (fmt_curr(max(1, cp - 15)), "arithmetic_mistake"),
        ]

    else:  # find_cp_from_sp_and_loss
        cp = random.choice([60, 100, 120, 150, 200, 300, 500])
        l = random.choice([10, 15, 20, 25, 30])
        sp = round(cp * (1 - l / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(cp)
        trap_add_l = fmt_curr(round(sp * (1 + l / 100), 2))
        q_text = f"An item is sold at a clearance price of ${sp}, incurring a {l}% loss. What was the cost price?"
        explanation = (
            f"Step 1: CP * (1 - {l}/100) = SP (${sp}).\n"
            f"Step 2: CP = ${sp} / {round(1 - l/100, 2)} = {correct}."
        )
        distractors = [
            (trap_add_l, "percentage_base_mistake"),
            (fmt_curr(round(sp / (1 + l / 100), 2)), "conceptual_mistake"),
            (fmt_curr(cp + 15), "arithmetic_mistake"),
            (fmt_curr(max(1, cp - 15)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="profit_loss_multipliers",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5033: markup
# =========================================================================
def markup(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "calculate_marked_price",
        "calculate_markup_percentage",
        "find_cost_price_from_markup",
        "markup_vs_margin",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "calculate_marked_price":
        cp = random.choice([40, 60, 80, 120, 150, 200, 300])
        m = random.choice([20, 25, 30, 40, 50, 60, 75, 100])
        mp = round(cp * (1 + m / 100), 2)
        if mp == int(mp):
            mp = int(mp)
        correct = fmt_curr(mp)
        q_text = f"A manufacturer produces a product for ${cp} and marks it up by {m}%. What is the marked price (list price)?"
        explanation = (
            f"Step 1: Marked Price (MP) = CP * (1 + Markup%/100).\n"
            f"Step 2: MP = ${cp} * (1 + {m}/100) = ${cp} * {1 + m/100} = {correct}."
        )
        distractors = [
            (fmt_curr(cp + m), "percentage_base_mistake"),
            (fmt_curr(round(cp * (m / 100), 2)), "careless_mistake"),
            (fmt_curr(mp + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, mp - 10)), "arithmetic_mistake"),
        ]

    elif variant == "calculate_markup_percentage":
        cp = random.choice([50, 80, 100, 120, 160, 200])
        m = random.choice([20, 25, 30, 40, 50, 60, 75, 100])
        mp = round(cp * (1 + m / 100), 2)
        if mp == int(mp):
            mp = int(mp)
        diff = mp - cp
        correct = fmt_pct(m)
        margin_pct = fmt_pct(round((diff / mp) * 100, 2))
        q_text = f"A boutique buys a handbag for ${cp} and tags it with a marked price of ${mp}. What is the markup percentage?"
        explanation = (
            f"Step 1: Markup Amount = MP - CP = ${mp} - ${cp} = ${diff}.\n"
            f"Step 2: Markup % is ALWAYS based on CP: (${diff} / ${cp}) * 100% = {correct}.\n"
            f"Trap Warning: Calculating over MP (${mp}) yields {margin_pct}, which is the profit margin, NOT the markup percentage!"
        )
        distractors = [
            (margin_pct, "percentage_base_mistake"),
            (fmt_curr(diff), "careless_mistake"),
            (fmt_pct(m + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, m - 5)), "arithmetic_mistake"),
        ]

    elif variant == "find_cost_price_from_markup":
        cp = random.choice([50, 80, 100, 150, 200, 250, 400])
        m = random.choice([20, 25, 30, 40, 50, 60, 75, 80])
        mp = round(cp * (1 + m / 100), 2)
        if mp == int(mp):
            mp = int(mp)
        correct = fmt_curr(cp)
        trap_sub_m = fmt_curr(round(mp * (1 - m / 100), 2))
        q_text = f"An antique vase has a marked price of ${mp}, which reflects a {m}% markup over its cost price. What was the cost price?"
        explanation = (
            f"Step 1: MP = CP * (1 + {m}/100).\n"
            f"Step 2: CP = ${mp} / {1 + m/100} = {correct}.\n"
            f"Trap Warning: Subtracting {m}% from MP gives {trap_sub_m}, which confuses markup on CP with discount on MP."
        )
        conceptual_cand = fmt_curr(round(mp / (1 - m / 100), 2)) if m < 100 else fmt_curr(round(mp * 0.75, 2))
        distractors = [
            (trap_sub_m, "percentage_base_mistake"),
            (conceptual_cand, "conceptual_mistake"),
            (fmt_curr(cp + 15), "arithmetic_mistake"),
            (fmt_curr(max(1, cp - 15)), "arithmetic_mistake"),
        ]

    else:  # markup_vs_margin
        cp = random.choice([40, 50, 80, 100, 200])
        m = random.choice([25, 50, 100])
        mp = round(cp * (1 + m / 100), 2)
        diff = mp - cp
        markup_pct = m
        margin_pct = round((diff / mp) * 100, 2)
        diff_pct = round(markup_pct - margin_pct, 2)
        correct = fmt_pct(diff_pct)
        q_text = (
            f"A product has a cost price of ${cp} and a marked price of ${mp}. "
            f"What is the difference (in percentage points) between the markup percentage (based on CP) and the margin percentage (based on MP)?"
        )
        explanation = (
            f"Step 1: Markup % (on CP) = (${diff} / ${cp}) * 100% = {fmt_pct(markup_pct)}.\n"
            f"Step 2: Margin % (on MP) = (${diff} / ${mp}) * 100% = {fmt_pct(margin_pct)}.\n"
            f"Step 3: Difference = {fmt_pct(markup_pct)} - {fmt_pct(margin_pct)} = {correct}."
        )
        distractors = [
            (fmt_pct(markup_pct), "careless_mistake"),
            (fmt_pct(margin_pct), "percentage_base_mistake"),
            (fmt_pct(diff_pct + 4), "arithmetic_mistake"),
            (fmt_pct(max(1.0, diff_pct - 4)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="markup",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5034: discount
# =========================================================================
def discount(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "calculate_discount_percentage",
        "find_selling_price_after_discount",
        "find_marked_price_from_discount",
        "discount_amount_from_percentage",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "calculate_discount_percentage":
        mp = random.choice([50, 80, 100, 120, 150, 200, 250, 300])
        d = random.choice([10, 15, 20, 25, 30, 40, 50])
        sp = round(mp * (1 - d / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        disc_amt = mp - sp
        correct = fmt_pct(d)
        trap_sp_base = fmt_pct(round((disc_amt / sp) * 100, 2))
        q_text = f"An item with a marked price of ${mp} is sold for ${sp}. What is the discount percentage?"
        explanation = (
            f"Step 1: Discount amount = MP - SP = ${mp} - ${sp} = ${disc_amt}.\n"
            f"Step 2: Discount % is ALWAYS calculated over Marked Price (MP): (${disc_amt} / ${mp}) * 100% = {correct}.\n"
            f"Trap: Dividing by SP (${sp}) gives {trap_sp_base}, which is a percentage base error!"
        )
        distractors = [
            (trap_sp_base, "percentage_base_mistake"),
            (fmt_curr(disc_amt), "careless_mistake"),
            (fmt_pct(d + 5), "arithmetic_mistake"),
            (fmt_pct(max(1.0, d - 5)), "arithmetic_mistake"),
        ]

    elif variant == "find_selling_price_after_discount":
        mp = random.choice([60, 80, 100, 120, 150, 180, 240, 320])
        d = random.choice([10, 15, 20, 25, 30, 40, 50])
        sp = round(mp * (1 - d / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(sp)
        disc_amt = mp - sp
        q_text = f"A store offers a {d}% discount on a watch with a marked price of ${mp}. What is the selling price?"
        explanation = (
            f"Step 1: Discount multiplier = (1 - {d}/100) = {round(1 - d/100, 2)}.\n"
            f"Step 2: Selling Price (SP) = ${mp} * {round(1 - d/100, 2)} = {correct}."
        )
        distractors = [
            (fmt_curr(disc_amt), "careless_mistake"),
            (fmt_curr(mp - d), "percentage_base_mistake"),
            (fmt_curr(sp + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, sp - 10)), "arithmetic_mistake"),
        ]

    elif variant == "find_marked_price_from_discount":
        mp = random.choice([80, 100, 120, 150, 200, 250, 400])
        d = random.choice([10, 15, 20, 25, 30, 40])
        sp = round(mp * (1 - d / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(mp)
        trap_add_d = fmt_curr(round(sp * (1 + d / 100), 2))
        q_text = f"After a {d}% discount, a customer buys a tennis racket for ${sp}. What was the marked price?"
        explanation = (
            f"Step 1: SP = MP * (1 - {d}/100) -> MP = SP / (1 - {d}/100).\n"
            f"Step 2: MP = ${sp} / {round(1 - d/100, 2)} = {correct}."
        )
        distractors = [
            (trap_add_d, "percentage_base_mistake"),
            (fmt_curr(round(sp / (1 + d / 100), 2)), "conceptual_mistake"),
            (fmt_curr(mp + 15), "arithmetic_mistake"),
            (fmt_curr(max(1, mp - 15)), "arithmetic_mistake"),
        ]

    else:  # discount_amount_from_percentage
        mp = random.choice([80, 120, 160, 200, 250, 300, 500])
        d = random.choice([10, 15, 20, 25, 30, 40])
        disc_amt = round(mp * (d / 100), 2)
        if disc_amt == int(disc_amt):
            disc_amt = int(disc_amt)
        sp = mp - disc_amt
        correct = fmt_curr(disc_amt)
        q_text = f"A suit marked at ${mp} is on sale with a {d}% discount. What is the total discount amount saved by the buyer?"
        explanation = (
            f"Step 1: Discount Amount = MP * (Discount%/100).\n"
            f"Step 2: Discount = ${mp} * ({d}/100) = {correct}."
        )
        distractors = [
            (fmt_curr(sp), "careless_mistake"),
            (fmt_curr(d), "percentage_base_mistake"),
            (fmt_curr(disc_amt + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, disc_amt - 10)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="discount",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5035: markup_discount_combined
# =========================================================================
def markup_discount_combined(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_net_profit_percentage",
        "find_sp_and_profit_given_cp",
        "breakeven_discount",
        "find_markup_needed_for_target_profit",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "find_net_profit_percentage":
        m = random.choice([25, 40, 50, 60, 80, 100])
        d = random.choice([10, 15, 20, 25, 30])
        mult = (1 + m / 100) * (1 - d / 100)
        net_pct = round((mult - 1) * 100, 2)
        label = "profit" if net_pct >= 0 else "loss"
        correct = f"{abs(net_pct):.2f}% {label}".replace(".00%", "%")
        simple_sub = m - d
        simple_str = f"{abs(simple_sub)}% {'profit' if simple_sub >= 0 else 'loss'}"
        q_text = (
            f"A merchant marks goods up by {m}% above cost price and then offers a discount of {d}% on the marked price. "
            f"What is the net profit or loss percentage?"
        )
        explanation = (
            f"Step 1: Multiplier chaining: (1 + Markup/100) * (1 - Discount/100) = {1 + m/100} * {round(1 - d/100, 2)} = {round(mult, 4)}.\n"
            f"Step 2: Net Profit % = ({round(mult, 4)} - 1) * 100% = {correct}.\n"
            f"Trap Warning: Simply subtracting {m}% - {d}% gives {simple_str}! Discount is applied to the marked price, which is higher than CP."
        )
        distractors = [
            (simple_str, "conceptual_mistake"),
            (f"{abs(net_pct):.2f}% {'loss' if label == 'profit' else 'profit'}".replace(".00%", "%"), "conceptual_mistake"),
            (f"{abs(net_pct) + 4:.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
            (f"{max(1.0, abs(net_pct) - 4):.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
        ]

    elif variant == "find_sp_and_profit_given_cp":
        cp = random.choice([50, 100, 150, 200, 250, 400])
        m = random.choice([30, 40, 50, 60])
        d = random.choice([10, 20, 25])
        mp = round(cp * (1 + m / 100), 2)
        sp = round(mp * (1 - d / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(sp)
        q_text = (
            f"A shopkeeper purchases an item for ${cp}, marks it up by {m}%, and then allows a discount of {d}%. "
            f"What is the final selling price?"
        )
        explanation = (
            f"Step 1: Find Marked Price (MP) = ${cp} * (1 + {m}/100) = ${mp}.\n"
            f"Step 2: Find Selling Price (SP) = ${mp} * (1 - {d}/100) = ${sp}."
        )
        distractors = [
            (fmt_curr(round(cp * (1 + (m - d) / 100), 2)), "conceptual_mistake"),
            (fmt_curr(mp), "percentage_base_mistake"),
            (fmt_curr(sp + 12), "arithmetic_mistake"),
            (fmt_curr(max(1, sp - 12)), "arithmetic_mistake"),
        ]

    elif variant == "breakeven_discount":
        m = random.choice([20, 25, 40, 50, 60, 100])
        be_disc = round((m / (100 + m)) * 100, 2)
        correct = fmt_pct(be_disc)
        q_text = (
            f"A retailer marks up all goods by {m}% over cost price. What maximum percentage discount can he offer "
            f"on the marked price without incurring a net loss (i.e., breakeven)?"
        )
        explanation = (
            f"Step 1: For breakeven, SP = CP. Let CP = 100, then MP = {100 + m}.\n"
            f"Step 2: Discount required = MP - CP = {100 + m} - 100 = {m}.\n"
            f"Step 3: Discount % = ({m} / {100 + m}) * 100% = {correct}.\n"
            f"GMAT Trap: Offering a {m}% discount would result in a significant loss! The discount base is {100 + m}, not 100."
        )
        distractors = [
            (fmt_pct(m), "conceptual_mistake"),
            (fmt_pct(round((m / 100) * 100, 2)), "percentage_base_mistake"),
            (fmt_pct(be_disc + 3), "arithmetic_mistake"),
            (fmt_pct(max(1.0, be_disc - 3)), "arithmetic_mistake"),
        ]

    else:  # find_markup_needed_for_target_profit
        p = random.choice([10, 12, 15, 20, 25])
        d = random.choice([10, 15, 20, 25])
        m_needed = round((((1 + p / 100) / (1 - d / 100)) - 1) * 100, 2)
        correct = fmt_pct(m_needed)
        simple_add = fmt_pct(p + d)
        q_text = (
            f"A merchant wants to offer a {d}% discount on the marked price while still earning a {p}% profit on cost price. "
            f"By what percentage must the goods be marked up over cost price?"
        )
        explanation = (
            f"Step 1: Relationship: CP * (1 + Markup/100) * (1 - Discount/100) = CP * (1 + Profit/100).\n"
            f"Step 2: (1 + Markup/100) = (1 + {p}/100) / (1 - {d}/100) = {1 + p/100} / {round(1 - d/100, 2)}.\n"
            f"Step 3: Markup % = ({1 + p/100} / {round(1 - d/100, 2)} - 1) * 100% = {correct}.\n"
            f"Trap Warning: Simply adding {p}% + {d}% gives {simple_add}, which is an arithmetic trap."
        )
        distractors = [
            (simple_add, "conceptual_mistake"),
            (fmt_pct(round((1 + p / 100) * (1 - d / 100) * 100 - 100, 2)), "percentage_base_mistake"),
            (fmt_pct(m_needed + 4), "arithmetic_mistake"),
            (fmt_pct(max(1.0, m_needed - 4)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="markup_discount_combined",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5036: successive_discounts
# =========================================================================
def successive_discounts(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_successive_discounts_equivalent",
        "final_sp_after_two_discounts",
        "compare_discount_schemes",
        "three_successive_discounts",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "two_successive_discounts_equivalent":
        d1 = random.choice([10, 15, 20, 25, 30, 40])
        d2 = random.choice([10, 15, 20, 25, 30])
        eq_disc = round(d1 + d2 - (d1 * d2) / 100, 2)
        correct = fmt_pct(eq_disc)
        simple_add = fmt_pct(d1 + d2)
        q_text = (
            f"Successive discounts of {d1}% and {d2}% are equivalent to a single discount of what percentage?"
        )
        explanation = (
            f"Step 1: Multiplier approach: (1 - {d1}/100) * (1 - {d2}/100) = {round(1 - d1/100, 2)} * {round(1 - d2/100, 2)} = {round((1-d1/100)*(1-d2/100), 4)}.\n"
            f"Step 2: Equivalent discount = 1 - {round((1-d1/100)*(1-d2/100), 4)} = {correct}.\n"
            f"Shortcut formula: d1 + d2 - (d1*d2)/100 = {d1} + {d2} - {d1*d2/100} = {correct}.\n"
            f"Trap: Do NOT just add {d1}% + {d2}% = {simple_add}!"
        )
        distractors = [
            (simple_add, "conceptual_mistake"),
            (fmt_pct(round(d1 + d2 + (d1 * d2) / 100, 2)), "percentage_base_mistake"),
            (fmt_pct(eq_disc + 2), "arithmetic_mistake"),
            (fmt_pct(max(1.0, eq_disc - 2)), "arithmetic_mistake"),
        ]

    elif variant == "final_sp_after_two_discounts":
        mp = random.choice([100, 150, 200, 250, 300, 400, 500])
        d1 = random.choice([10, 20, 25, 30])
        d2 = random.choice([10, 15, 20])
        sp = round(mp * (1 - d1 / 100) * (1 - d2 / 100), 2)
        if sp == int(sp):
            sp = int(sp)
        correct = fmt_curr(sp)
        q_text = (
            f"An electronic gadget marked at ${mp} is sold with successive discounts of {d1}% and {d2}%. "
            f"What is the final selling price?"
        )
        explanation = (
            f"Step 1: Price after 1st discount ({d1}%): ${mp} * {round(1 - d1/100, 2)} = ${round(mp * (1 - d1/100), 2)}.\n"
            f"Step 2: Price after 2nd discount ({d2}%): ${round(mp * (1 - d1/100), 2)} * {round(1 - d2/100, 2)} = {correct}."
        )
        distractors = [
            (fmt_curr(round(mp * (1 - (d1 + d2) / 100), 2)), "conceptual_mistake"),
            (fmt_curr(round(mp - sp, 2)), "careless_mistake"),
            (fmt_curr(sp + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, sp - 10)), "arithmetic_mistake"),
        ]

    elif variant == "compare_discount_schemes":
        mp = random.choice([200, 400, 500, 800, 1000])
        d1 = random.choice([20, 25, 30])
        d2 = random.choice([10, 15, 20])
        single_s = d1 + d2
        diff_save = round(mp * (d1 * d2) / 10000, 2)
        if diff_save == int(diff_save):
            diff_save = int(diff_save)
        correct = fmt_curr(diff_save)
        q_text = (
            f"A customer can choose between Scheme A: a single discount of {single_s}%, and Scheme B: successive discounts "
            f"of {d1}% and {d2}%. On an item marked at ${mp}, how much more does Scheme A save compared to Scheme B?"
        )
        explanation = (
            f"Step 1: Scheme A discount % = {single_s}%.\n"
            f"Step 2: Scheme B discount % = {d1} + {d2} - ({d1}*{d2})/100 = {single_s} - {round(d1*d2/100, 2)}%.\n"
            f"Step 3: Difference in discount percentage = {round(d1*d2/100, 2)}%.\n"
            f"Step 4: Difference in dollars = ${mp} * ({round(d1*d2/100, 2)}/100) = {correct}.\n"
            f"GMAT Trap: Believing both schemes are identical because {d1} + {d2} = {single_s}!"
        )
        distractors = [
            ("$0 (Both schemes save the same)", "conceptual_mistake"),
            (fmt_curr(round(mp * (single_s / 100), 2)), "careless_mistake"),
            (fmt_curr(diff_save + 10), "arithmetic_mistake"),
            (fmt_curr(max(1, diff_save - 5)), "arithmetic_mistake"),
        ]

    else:  # three_successive_discounts
        d1 = random.choice([10, 20])
        d2 = random.choice([10, 15, 20])
        d3 = random.choice([5, 10])
        mult = (1 - d1 / 100) * (1 - d2 / 100) * (1 - d3 / 100)
        eq_disc = round((1 - mult) * 100, 2)
        correct = fmt_pct(eq_disc)
        simple_sum = fmt_pct(d1 + d2 + d3)
        q_text = (
            f"What single discount percentage is equivalent to three successive discounts of {d1}%, {d2}%, and {d3}%?"
        )
        explanation = (
            f"Step 1: Factor multiplication: (1 - {d1}/100) * (1 - {d2}/100) * (1 - {d3}/100) = {round(mult, 4)}.\n"
            f"Step 2: Equivalent discount = (1 - {round(mult, 4)}) * 100% = {correct}."
        )
        distractors = [
            (simple_sum, "conceptual_mistake"),
            (fmt_pct(round(d1 + d2 - (d1 * d2) / 100, 2)), "percentage_base_mistake"),
            (fmt_pct(eq_disc + 2), "arithmetic_mistake"),
            (fmt_pct(max(1.0, eq_disc - 2)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="successive_discounts",
        subvariant=variant,
    )


# =========================================================================
# Pattern 5037: percentage_vs_percentage_points
# =========================================================================
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


# =========================================================================
# Pattern 5038: more_than_vs_less_than
# =========================================================================
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


# =========================================================================
# Pattern 5039: percentage_word_problems
# =========================================================================
def percentage_word_problems(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "demographics_and_subgroups",
        "salary_and_remainder_budget",
        "exam_score_and_passing_threshold",
        "revenue_cost_profit_growth",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "demographics_and_subgroups":
        n = random.choice([600, 800, 1000, 1200, 1500, 2000])
        p1 = random.choice([30, 40, 50, 60])
        p2 = random.choice([20, 25, 40, 50])
        subgroup1 = (n * p1) // 100
        ans = (subgroup1 * p2) // 100
        correct = fmt_num(ans)
        q_text = (
            f"In a corporation of {n:,} employees, {p1}% work in the engineering division. "
            f"Among the engineers, {p2}% hold a master's degree. "
            f"How many employees in the corporation are engineers with a master's degree?"
        )
        explanation = (
            f"Step 1: Number of engineers = {p1}% of {n:,} = ({p1}/100) * {n} = {subgroup1}.\n"
            f"Step 2: Engineers with master's degrees = {p2}% of {subgroup1} = ({p2}/100) * {subgroup1} = {ans}.\n"
            f"Alternatively, combine percentages: ({p1}/100) * ({p2}/100) * {n} = {ans}."
        )
        distractors = [
            (fmt_num(round(n * (p1 + p2) / 100)), "percentage_base_mistake"),
            (fmt_num(subgroup1), "careless_mistake"),
            (fmt_num(ans + 20), "arithmetic_mistake"),
            (fmt_num(max(5, ans - 20)), "arithmetic_mistake"),
        ]

    elif variant == "salary_and_remainder_budget":
        p1 = random.choice([20, 25, 30, 40])
        p2 = random.choice([20, 30, 40, 50])
        # Leftover fraction = (1 - p1/100) * (1 - p2/100)
        frac_rem = (1 - p1 / 100) * (1 - p2 / 100)
        total_income = random.choice([4000, 5000, 6000, 8000, 10000])
        savings = int(round(total_income * frac_rem))
        correct = fmt_curr(total_income)
        trap_sum_pct = fmt_curr(round(savings / (1 - (p1 + p2) / 100)))
        q_text = (
            f"An analyst spends {p1}% of monthly salary on rent. Of the remainder, {p2}% is spent on food and utilities. "
            f"If the analyst saves the remaining ${savings:,} each month, what is the analyst's total monthly salary?"
        )
        explanation = (
            f"Step 1: After rent ({p1}%), remaining salary = 100% - {p1}% = {100 - p1}% = {round(1 - p1/100, 2)} of total.\n"
            f"Step 2: Food & utilities take {p2}% of remainder, leaving 100% - {p2}% = {100 - p2}% of remainder.\n"
            f"Step 3: Total leftover fraction = {round(1 - p1/100, 2)} * {round(1 - p2/100, 2)} = {round(frac_rem, 4)}.\n"
            f"Step 4: Total Salary = ${savings:,} / {round(frac_rem, 4)} = {correct}.\n"
            f"GMAT Trap: Adding {p1}% + {p2}% = {p1+p2}% and calculating ${savings:,} / {1 - (p1+p2)/100} gives {trap_sum_pct}, which wrongly assumes {p2}% was of total salary!"
        )
        distractors = [
            (trap_sum_pct, "percentage_base_mistake"),
            (fmt_curr(round(savings * (1 + (p1 + p2) / 100))), "conceptual_mistake"),
            (fmt_curr(total_income + 1000), "arithmetic_mistake"),
            (fmt_curr(max(500, total_income - 1000)), "arithmetic_mistake"),
        ]

    elif variant == "exam_score_and_passing_threshold":
        pct_pass = random.choice([35, 40, 50, 60])
        max_marks = random.choice([400, 500, 600, 800, 1000])
        pass_marks = int(max_marks * (pct_pass / 100))
        fail_by = random.choice([15, 20, 25, 30, 40])
        scored = pass_marks - fail_by
        correct = fmt_num(max_marks)
        q_text = (
            f"A candidate takes an examination where the passing requirement is {pct_pass}% of the maximum marks. "
            f"If the candidate scores {scored} marks and fails by {fail_by} marks, what is the maximum marks of the examination?"
        )
        explanation = (
            f"Step 1: Passing marks = Scored + Shortfall = {scored} + {fail_by} = {pass_marks}.\n"
            f"Step 2: Since {pct_pass}% of Maximum Marks = {pass_marks}, Maximum Marks = {pass_marks} / ({pct_pass}/100) = {correct}."
        )
        distractors = [
            (fmt_num(round((scored - fail_by) / (pct_pass / 100))), "setup_mistake"),
            (fmt_num(round(scored / (pct_pass / 100))), "careless_mistake"),
            (fmt_num(max_marks + 100), "arithmetic_mistake"),
            (fmt_num(max(100, max_marks - 100)), "arithmetic_mistake"),
        ]

    else:  # revenue_cost_profit_growth
        r = 500000
        c = 300000
        r_growth = random.choice([10, 20, 25])
        c_drop = random.choice([10, 15, 20])
        new_r = round(r * (1 + r_growth / 100))
        new_c = round(c * (1 - c_drop / 100))
        new_profit = new_r - new_c
        correct = fmt_curr(new_profit)
        q_text = (
            f"In year 1, a firm had revenue of ${r:,} and operating costs of ${c:,}. "
            f"In year 2, revenue increased by {r_growth}% while costs decreased by {c_drop}%. "
            f"What was the firm's operating profit in year 2?"
        )
        explanation = (
            f"Step 1: Year 2 Revenue = ${r:,} * (1 + {r_growth}/100) = ${new_r:,}.\n"
            f"Step 2: Year 2 Costs = ${c:,} * (1 - {c_drop}/100) = ${new_c:,}.\n"
            f"Step 3: Year 2 Profit = Revenue - Costs = ${new_r:,} - ${new_c:,} = {correct}."
        )
        distractors = [
            (fmt_curr(round((r - c) * (1 + (r_growth + c_drop) / 100))), "percentage_base_mistake"),
            (fmt_curr(round(new_r - c)), "careless_mistake"),
            (fmt_curr(new_profit + 25000), "arithmetic_mistake"),
            (fmt_curr(max(1000, new_profit - 25000)), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="percentage_word_problems",
        subvariant=variant,
    )


# =========================================================================
# Aliases and Metadata Registry
# =========================================================================
generate_percentage_fundamentals = percentage_fundamentals
generate_percentage_increase = percentage_increase
generate_percentage_decrease = percentage_decrease
generate_new_value_percentage_change = new_value_percentage_change
generate_reverse_percentage = reverse_percentage
generate_successive_percentage_changes = successive_percentage_changes
generate_profit_and_loss = profit_and_loss
generate_profit_loss_multipliers = profit_loss_multipliers
generate_markup = markup
generate_discount = discount
generate_markup_discount_combined = markup_discount_combined
generate_successive_discounts = successive_discounts
generate_percentage_vs_percentage_points = percentage_vs_percentage_points
generate_more_than_vs_less_than = more_than_vs_less_than
generate_percentage_word_problems = percentage_word_problems

DAY3_GENERATORS = {
    5025: percentage_fundamentals,
    "5025": percentage_fundamentals,
    "percentage_fundamentals": percentage_fundamentals,
    5026: percentage_increase,
    "5026": percentage_increase,
    "percentage_increase": percentage_increase,
    5027: percentage_decrease,
    "5027": percentage_decrease,
    "percentage_decrease": percentage_decrease,
    5028: new_value_percentage_change,
    "5028": new_value_percentage_change,
    "new_value_percentage_change": new_value_percentage_change,
    5029: reverse_percentage,
    "5029": reverse_percentage,
    "reverse_percentage": reverse_percentage,
    5030: successive_percentage_changes,
    "5030": successive_percentage_changes,
    "successive_percentage_changes": successive_percentage_changes,
    5031: profit_and_loss,
    "5031": profit_and_loss,
    "profit_and_loss": profit_and_loss,
    5032: profit_loss_multipliers,
    "5032": profit_loss_multipliers,
    "profit_loss_multipliers": profit_loss_multipliers,
    5033: markup,
    "5033": markup,
    "markup": markup,
    5034: discount,
    "5034": discount,
    "discount": discount,
    5035: markup_discount_combined,
    "5035": markup_discount_combined,
    "markup_discount_combined": markup_discount_combined,
    5036: successive_discounts,
    "5036": successive_discounts,
    "successive_discounts": successive_discounts,
    5037: percentage_vs_percentage_points,
    "5037": percentage_vs_percentage_points,
    "percentage_vs_percentage_points": percentage_vs_percentage_points,
    5038: more_than_vs_less_than,
    "5038": more_than_vs_less_than,
    "more_than_vs_less_than": more_than_vs_less_than,
    5039: percentage_word_problems,
    "5039": percentage_word_problems,
    "percentage_word_problems": percentage_word_problems,
}

DAY3_PATTERNS_METADATA = {
    5025: {
        "id": 5025,
        "name": "percentage_fundamentals",
        "description": "Find x% of N, what % A is of B, find original number given x% of N = A, and fraction-to-percentage conversions.",
        "variants": [
            "find_percentage_of_number",
            "what_percentage_is_a_of_b",
            "find_base_from_percentage",
            "fraction_to_percentage",
        ],
    },
    5026: {
        "id": 5026,
        "name": "percentage_increase",
        "description": "Percentage increase calculations across price, population, salary, and revenue using original as base.",
        "variants": [
            "price_increase",
            "population_growth",
            "salary_hike",
            "revenue_expansion",
        ],
    },
    5027: {
        "id": 5027,
        "name": "percentage_decrease",
        "description": "Percentage decrease calculations using original value as denominator base.",
        "variants": [
            "price_reduction",
            "population_decline",
            "budget_cut",
            "inventory_depletion",
        ],
    },
    5028: {
        "id": 5028,
        "name": "new_value_percentage_change",
        "description": "Multipliers (1 + r/100) and (1 - r/100) for benchmark and general percentage changes.",
        "variants": [
            "new_value_after_increase",
            "new_value_after_decrease",
            "benchmark_multiplier",
            "multi_step_or_decimal_change",
        ],
    },
    5029: {
        "id": 5029,
        "name": "reverse_percentage",
        "description": "Finding original value from value after percentage change (Original = New / (1 ± r/100)).",
        "variants": [
            "original_price_after_discount",
            "original_salary_after_raise",
            "price_before_sales_tax",
            "original_population_before_change",
        ],
    },
    5030: {
        "id": 5030,
        "name": "successive_percentage_changes",
        "description": "Multiplier chaining for sequential percentage changes and the symmetric +x% / -x% trap.",
        "variants": [
            "two_increases",
            "increase_then_decrease",
            "symmetric_change_trap",
            "three_successive_changes",
        ],
    },
    5031: {
        "id": 5031,
        "name": "profit_and_loss",
        "description": "Cost Price (CP), Selling Price (SP), Profit/Loss amounts and percentages calculated on CP.",
        "variants": [
            "calculate_profit_percentage",
            "calculate_loss_percentage",
            "profit_with_overhead",
            "sp_per_unit_vs_cp",
        ],
    },
    5032: {
        "id": 5032,
        "name": "profit_loss_multipliers",
        "description": "Direct profit and loss multipliers: SP = CP(1 ± r/100) and finding CP = SP / (1 ± r/100).",
        "variants": [
            "find_sp_from_cp_and_profit",
            "find_sp_from_cp_and_loss",
            "find_cp_from_sp_and_profit",
            "find_cp_from_sp_and_loss",
        ],
    },
    5033: {
        "id": 5033,
        "name": "markup",
        "description": "Marked price from cost price and markup percentage, and markup vs profit margin distinction.",
        "variants": [
            "calculate_marked_price",
            "calculate_markup_percentage",
            "find_cost_price_from_markup",
            "markup_vs_margin",
        ],
    },
    5034: {
        "id": 5034,
        "name": "discount",
        "description": "Discounts and discount percentages calculated on Marked Price (MP), and finding SP/MP.",
        "variants": [
            "calculate_discount_percentage",
            "find_selling_price_after_discount",
            "find_marked_price_from_discount",
            "discount_amount_from_percentage",
        ],
    },
    5035: {
        "id": 5035,
        "name": "markup_discount_combined",
        "description": "CP -> markup -> MP -> discount -> SP and net profit/loss percentage calculations.",
        "variants": [
            "find_net_profit_percentage",
            "find_sp_and_profit_given_cp",
            "breakeven_discount",
            "find_markup_needed_for_target_profit",
        ],
    },
    5036: {
        "id": 5036,
        "name": "successive_discounts",
        "description": "Successive discount chaining MP * (1 - d1) * (1 - d2) and eliminating simple addition trap.",
        "variants": [
            "two_successive_discounts_equivalent",
            "final_sp_after_two_discounts",
            "compare_discount_schemes",
            "three_successive_discounts",
        ],
    },
    5037: {
        "id": 5037,
        "name": "percentage_vs_percentage_points",
        "description": "Trap distinction between change in percentage points and relative percentage change.",
        "variants": [
            "percentage_points_vs_percent_increase",
            "percentage_points_vs_percent_decrease",
            "interest_rate_change",
            "identify_correct_statement",
        ],
    },
    5038: {
        "id": 5038,
        "name": "more_than_vs_less_than",
        "description": "Relative percentage comparisons: 'A is what % more than B' vs 'B is what % less than A'.",
        "variants": [
            "a_more_than_b_direct",
            "b_less_than_a_direct",
            "a_is_x_percent_more_then_b_is_what_less",
            "a_is_x_percent_less_then_b_is_what_more",
        ],
    },
    5039: {
        "id": 5039,
        "name": "percentage_word_problems",
        "description": "Multi-step GMAT applications: demographics, remainder budgets, exam pass thresholds, and growth.",
        "variants": [
            "demographics_and_subgroups",
            "salary_and_remainder_budget",
            "exam_score_and_passing_threshold",
            "revenue_cost_profit_growth",
        ],
    },
}
