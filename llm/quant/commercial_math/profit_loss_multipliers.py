import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

