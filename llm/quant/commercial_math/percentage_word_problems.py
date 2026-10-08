import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

