import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

