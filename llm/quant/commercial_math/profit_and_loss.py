import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

