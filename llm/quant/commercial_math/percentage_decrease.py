import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

