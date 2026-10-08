from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_ratio_with_total(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_parts_find_one",
        "two_parts_difference",
        "three_parts_find_one",
        "three_parts_extremes_diff",
        "ratio_with_total_word_problem",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "two_parts_find_one":
        m = random.randint(2, 5)
        n = random.randint(3, 7)
        while gcd(m, n) != 1:
            n = random.randint(3, 7)
        k = random.randint(10, 50) if level <= 3 else random.randint(50, 150)
        tot = (m + n) * k
        share_a = m * k
        share_b = n * k
        question = (
            f"An amount of ${tot} is divided between Alice and Bob in the ratio {m}:{n}. "
            f"How much does Alice receive?"
        )
        correct = f"${share_a}"
        distractors = [f"${share_b}", f"${k}", f"${m * n}"]
        trap_map = {
            f"${share_b}": "careless_mistake",
            f"${k}": "setup_mistake",
            f"${m * n}": "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Sum of ratio parts = {m} + {n} = {m + n}.\n"
            f"Step 2: Value per part = ${tot} / {m + n} = ${k}.\n"
            f"Step 3: Alice's share = {m} parts * ${k} = ${share_a}."
        )

    elif subvariant == "two_parts_difference":
        m = random.randint(4, 8)
        n = random.randint(2, m - 1)
        while gcd(m, n) != 1:
            n = random.randint(2, m - 1)
        k = random.randint(12, 40)
        tot = (m + n) * k
        diff = (m - n) * k
        share_a = m * k
        question = (
            f"A total prize of ${tot} is shared between Partner A and Partner B in the ratio {m}:{n}. "
            f"What is the difference between the two shares?"
        )
        correct = f"${diff}"
        distractors = [f"${share_a}", f"${n * k}", f"${m - n}"]
        trap_map = {
            f"${share_a}": "careless_mistake",
            f"${n * k}": "careless_mistake",
            f"${m - n}": "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Total parts = {m} + {n} = {m + n}.\n"
            f"Step 2: Value of 1 part = ${tot} / {m + n} = ${k}.\n"
            f"Step 3: Difference in parts = {m} - {n} = {m - n}.\n"
            f"Step 4: Difference in dollars = {m - n} * ${k} = ${diff}."
        )

    elif subvariant == "three_parts_find_one":
        a, b, c = random.choice([(2, 3, 5), (3, 4, 7), (1, 4, 5), (2, 5, 8)])
        k = random.randint(15, 60)
        tot = (a + b + c) * k
        share_b = b * k
        question = (
            f"A sum of ${tot} is divided among three charities X, Y, and Z in the ratio {a}:{b}:{c}. "
            f"How much does charity Y receive?"
        )
        correct = f"${share_b}"
        distractors = [f"${a * k}", f"${c * k}", f"${k}"]
        trap_map = {
            f"${a * k}": "careless_mistake",
            f"${c * k}": "careless_mistake",
            f"${k}": "setup_mistake",
        }
        explanation = (
            f"Step 1: Sum of ratio parts = {a} + {b} + {c} = {a + b + c}.\n"
            f"Step 2: Value per part = ${tot} / {a + b + c} = ${k}.\n"
            f"Step 3: Charity Y receives {b} parts = {b} * ${k} = ${share_b}."
        )

    elif subvariant == "three_parts_extremes_diff":
        a, b, c = random.choice([(2, 5, 9), (3, 5, 8), (1, 3, 6), (2, 4, 7)])
        k = random.randint(10, 45)
        tot = (a + b + c) * k
        diff_extremes = (c - a) * k
        question = (
            f"A bonus pool of ${tot} is distributed among three employees in the ratio {a}:{b}:{c}. "
            f"What is the difference between the largest share and the smallest share?"
        )
        correct = f"${diff_extremes}"
        distractors = [f"${c * k}", f"${(c - b) * k}", f"${(b - a) * k}"]
        trap_map = {
            f"${c * k}": "careless_mistake",
            f"${(c - b) * k}": "setup_mistake",
            f"${(b - a) * k}": "setup_mistake",
        }
        explanation = (
            f"Step 1: Total parts = {a} + {b} + {c} = {a + b + c}.\n"
            f"Step 2: Value of 1 part = ${tot} / {a + b + c} = ${k}.\n"
            f"Step 3: Largest share has {c} parts; smallest has {a} parts. Difference = {c - a} parts.\n"
            f"Step 4: Dollar difference = {c - a} * ${k} = ${diff_extremes}."
        )

    else:  # ratio_with_total_word_problem
        # Chemistry alloy / mixture problem
        m, n = random.choice([(3, 2), (5, 3), (7, 3), (4, 1)])
        k = random.randint(8, 25)
        total_wt = (m + n) * k
        ans = m * k
        question = (
            f"An alloy of total weight {total_wt} kg consists only of copper and zinc in the ratio {m}:{n}. "
            f"How many kilograms of copper are in this alloy?"
        )
        correct = f"{ans} kg"
        distractors = [f"{n * k} kg", f"{k} kg", f"{total_wt - k} kg"]
        trap_map = {
            f"{n * k} kg": "careless_mistake",
            f"{k} kg": "setup_mistake",
            f"{total_wt - k} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total ratio parts = {m} + {n} = {m + n}.\n"
            f"Step 2: Mass per part = {total_wt} / {m + n} = {k} kg.\n"
            f"Step 3: Mass of copper = {m} * {k} = {ans} kg."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="ratio_with_total",
        subvariant=subvariant,
    )

