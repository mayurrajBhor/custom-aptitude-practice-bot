import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

