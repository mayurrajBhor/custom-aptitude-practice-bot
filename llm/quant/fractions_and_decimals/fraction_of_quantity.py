import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

from llm.common import (
    GMAT_BENCHMARK_FRACTIONS,
    clamp_level,
    gcd,
    lcm,
    make_mcq,
    make_options,
)
from .common import _clean_distractors, _format_frac, _format_mixed

def generate_fraction_of_quantity(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["direct_quantity", "word_problem", "reverse_quantity"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "direct_quantity":
        if level <= 2:
            den = random.choice([3, 4, 5, 8, 10])
            num = random.randint(1, den - 1)
            k = random.randint(5, 15)
        elif level <= 4:
            den = random.choice([6, 7, 8, 12, 15])
            num = random.randint(2, den - 1)
            k = random.randint(10, 30)
        else:
            den = random.choice([11, 13, 14, 16, 20])
            num = random.randint(3, den - 1)
            k = random.randint(20, 50)

        total = k * den
        ans = k * num
        correct = str(ans)

        candidates = [
            (str(ans + k), "arithmetic_mistake"),
            (str(ans - k), "arithmetic_mistake"),
            (str(total - ans), "careless_mistake"),
            (str((total // num) * den if num > 0 else total), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is {num}/{den} of {total}?"
        expl = (
            f"Step 1: Divide the quantity by the denominator to find 1 part: {total} ÷ {den} = {k}.\n"
            f"Step 2: Multiply by the numerator: {k} × {num} = {ans}.\n"
            f"Thus, {num}/{den} of {total} is {correct}."
        )

    elif variant == "word_problem":
        items = random.choice(["books", "laptops", "scholarship funds", "candies", "tickets"])
        den = random.choice([4, 5, 8, 10])
        num = random.randint(1, den - 1)
        k = random.randint(10, 40)
        total = k * den

        used_qty = num * k
        remaining_qty = total - used_qty
        correct = str(remaining_qty)

        candidates = [
            (str(used_qty), "careless_mistake"),
            (str(remaining_qty + k), "arithmetic_mistake"),
            (str(remaining_qty - k), "arithmetic_mistake"),
            (str(total - num), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = (
            f"A school library received an inventory of {total} {items}. "
            f"During the first week, {num}/{den} of the total {items} were checked out. "
            f"How many {items} REMAIN in the library?"
        )
        expl = (
            f"Step 1: Calculate the quantity checked out: ({num}/{den}) × {total} = {num} × {k} = {used_qty}.\n"
            f"Step 2: Subtract the checked-out items from the total inventory: {total} - {used_qty} = {remaining_qty}.\n"
            f"Common Trap: Answering {used_qty} answers how many were checked out, not how many remain!"
        )

    else:  # reverse_quantity
        den = random.choice([3, 4, 5, 7, 8])
        num = random.randint(2, den - 1)
        k = random.randint(6, 18)
        part = k * num
        original = k * den
        correct = str(original)

        candidates = [
            (str(part * num // den), "formula_selection_mistake"),
            (str(part * den), "conceptual_mistake"),
            (str(original + den), "arithmetic_mistake"),
            (str(original - den), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"If {num}/{den} of a mystery number is {part}, what is the original number?"
        expl = (
            f"Step 1: Set up the equation: ({num}/{den}) × N = {part}.\n"
            f"Step 2: Solve for N by multiplying both sides by the reciprocal {den}/{num}:\n"
            f"  N = {part} × ({den}/{num}) = ({part} ÷ {num}) × {den} = {k} × {den} = {original}.\n"
            f"Thus, the original number is {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_of_quantity",
        subvariant=variant,
    )

