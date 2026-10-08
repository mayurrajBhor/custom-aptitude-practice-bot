import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

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

