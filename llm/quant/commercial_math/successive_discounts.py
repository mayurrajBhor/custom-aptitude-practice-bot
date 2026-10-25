import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

