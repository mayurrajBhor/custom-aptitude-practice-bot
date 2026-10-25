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

def generate_fraction_simplification(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["reduce_lowest_terms", "identify_simplified", "gcd_simplification"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "reduce_lowest_terms":
        if level <= 2:
            g = random.randint(2, 5)
            a = random.randint(1, 4)
            b = random.randint(a + 1, 7)
        elif level <= 4:
            g = random.choice([4, 6, 8, 9, 12, 14])
            a = random.randint(2, 7)
            b = random.randint(a + 1, 11)
        else:
            g = random.choice([13, 17, 19, 21, 24])
            a = random.randint(3, 9)
            b = random.randint(a + 1, 15)

        while math.gcd(a, b) > 1:
            b += 1

        n = a * g
        d = b * g
        correct = f"{a}/{b}"

        candidates = [
            (f"{b}/{a}", "careless_mistake"),
            (f"{a + 1}/{b}", "arithmetic_mistake"),
            (f"{a}/{b + 1}", "arithmetic_mistake"),
        ]
        # Incomplete reduction distractor if g has a proper divisor
        divs = [x for x in [2, 3, 4] if g % x == 0 and g // x > 1]
        if divs:
            sub_d = divs[0]
            candidates.insert(0, (f"{a * sub_d}/{b * sub_d}", "conceptual_mistake"))
        else:
            candidates.insert(0, (f"{n - g}/{d - g}", "conceptual_mistake"))

        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Reduce the fraction {n}/{d} to its lowest (simplest) terms."
        expl = (
            f"Step 1: Find the greatest common divisor: GCD({n}, {d}) = {g}.\n"
            f"Step 2: Divide both numerator and denominator by {g}:\n"
            f"  {n} ÷ {g} = {a}\n"
            f"  {d} ÷ {g} = {b}\n"
            f"Since GCD({a}, {b}) = 1, the fraction cannot be simplified further.\n"
            f"Thus, {n}/{d} in lowest terms is {correct}."
        )

    elif variant == "identify_simplified":
        # Exactly one fraction is already in simplest terms
        a = random.randint(3, 8)
        b = random.randint(a + 1, 13)
        while math.gcd(a, b) > 1:
            b += 1
        correct = f"{a}/{b}"

        # 3 fractions that can be reduced
        c1 = f"{2 * 3}/{2 * 5}"  # 6/10
        c2 = f"{3 * 4}/{3 * 7}"  # 12/21
        c3 = f"{5 * 2}/{5 * 3}"  # 10/15
        if correct in [c1, c2, c3]:
            c1 = f"{4 * 2}/{4 * 7}"

        candidates = [
            (c1, "conceptual_mistake"),
            (c2, "conceptual_mistake"),
            (c3, "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Which of the following fractions is already in lowest terms (cannot be reduced further)?"
        expl = (
            f"A fraction is in lowest terms when the GCD of its numerator and denominator is 1.\n"
            f"For {correct}, GCD({a}, {b}) = 1, so it cannot be reduced.\n"
            f"All other options share common factors greater than 1 (e.g. {c1} shares factor 2, {c2} shares 3, {c3} shares 5)."
        )

    else:  # gcd_simplification
        if level <= 2:
            g = random.randint(3, 6)
            a = random.randint(1, 4)
            b = random.randint(a + 1, 7)
        elif level <= 4:
            g = random.choice([6, 8, 12, 14, 15])
            a = random.randint(2, 6)
            b = random.randint(a + 1, 9)
        else:
            g = random.choice([16, 18, 24, 28, 32])
            a = random.randint(3, 7)
            b = random.randint(a + 1, 11)

        while math.gcd(a, b) > 1:
            b += 1

        n = a * g
        d = b * g
        correct = str(g)

        candidates = [
            (str(g + 2), "arithmetic_mistake"),
            (str(max(1, g - 2)), "arithmetic_mistake"),
            (str(abs(n - d)), "careless_mistake"),
        ]
        divs = [x for x in [2, 3, 4] if g % x == 0 and g != x]
        if divs:
            candidates.insert(0, (str(divs[0]), "conceptual_mistake"))
        else:
            candidates.insert(0, (str(g // 2 if g > 2 else 1), "conceptual_mistake"))

        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = (
            f"What is the greatest common divisor (GCD) that should be used to reduce "
            f"{n}/{d} to its simplest form in a single step?"
        )
        expl = (
            f"To reduce {n}/{d} in a single step, divide both terms by their Greatest Common Divisor.\n"
            f"Factors of {n}: {n} = {g} × {a}\n"
            f"Factors of {d}: {d} = {g} × {b}\n"
            f"Since GCD({a}, {b}) = 1, GCD({n}, {d}) = {g}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_simplification",
        subvariant=variant,
    )

