import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

