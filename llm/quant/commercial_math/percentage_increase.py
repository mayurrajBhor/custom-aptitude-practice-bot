import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

