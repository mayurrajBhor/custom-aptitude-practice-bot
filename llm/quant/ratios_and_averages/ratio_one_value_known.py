from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_ratio_one_value_known(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "first_known_find_second",
        "second_known_find_first",
        "one_known_find_total",
        "one_known_find_difference",
        "three_way_one_known",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "first_known_find_second":
        m = random.randint(2, 6)
        n = random.randint(3, 8)
        while gcd(m, n) != 1:
            n = random.randint(3, 8)
        k = random.randint(5, 25)
        val_a = m * k
        val_b = n * k
        question = (
            f"The ratio of red marbles to blue marbles in a jar is {m}:{n}. "
            f"If there are {val_a} red marbles, how many blue marbles are there?"
        )
        correct = str(val_b)
        distractors = [str(val_a), str(k), str(int(val_a * m / n))]
        trap_map = {
            str(val_a): "careless_mistake",
            str(k): "setup_mistake",
            str(int(val_a * m / n)): "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Set up the proportion: Red / Blue = {m} / {n}.\n"
            f"Step 2: Since Red = {val_a}, the scale factor is {val_a} / {m} = {k}.\n"
            f"Step 3: Blue = {n} * {k} = {val_b}."
        )

    elif subvariant == "second_known_find_first":
        m = random.randint(3, 7)
        n = random.randint(2, 6)
        while gcd(m, n) != 1:
            n = random.randint(2, 6)
        k = random.randint(6, 30)
        val_b = n * k
        val_a = m * k
        question = (
            f"The ratio of managers to analysts at a consultancy is {m}:{n}. "
            f"If there are {val_b} analysts, how many managers are there?"
        )
        correct = str(val_a)
        distractors = [str(val_b), str(k), str(val_a + k)]
        trap_map = {
            str(val_b): "careless_mistake",
            str(k): "setup_mistake",
            str(val_a + k): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Ratio of Managers / Analysts = {m} / {n}.\n"
            f"Step 2: Scale factor = {val_b} / {n} = {k}.\n"
            f"Step 3: Managers = {m} * {k} = {val_a}."
        )

    elif subvariant == "one_known_find_total":
        m = random.randint(2, 5)
        n = random.randint(3, 7)
        while gcd(m, n) != 1:
            n = random.randint(3, 7)
        k = random.randint(7, 24)
        val_a = m * k
        total = (m + n) * k
        question = (
            f"The ratio of fiction books to non-fiction books in a library section is {m}:{n}. "
            f"If there are {val_a} fiction books, what is the total number of books in this section?"
        )
        correct = str(total)
        distractors = [str(n * k), str(total - k), str(val_a * 2)]
        trap_map = {
            str(n * k): "careless_mistake",
            str(total - k): "arithmetic_mistake",
            str(val_a * 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Scale factor = {val_a} / {m} = {k}.\n"
            f"Step 2: Total parts = {m} + {n} = {m + n}.\n"
            f"Step 3: Total books = ({m + n}) * {k} = {total}."
        )

    elif subvariant == "one_known_find_difference":
        m = random.randint(5, 9)
        n = random.randint(2, m - 1)
        while gcd(m, n) != 1:
            n = random.randint(2, m - 1)
        k = random.randint(8, 28)
        val_a = m * k
        diff = (m - n) * k
        question = (
            f"In an auditorium, the ratio of adults to children is {m}:{n}. "
            f"If there are {val_a} adults, how many more adults are there than children?"
        )
        correct = str(diff)
        distractors = [str(n * k), str(val_a), str(m - n)]
        trap_map = {
            str(n * k): "careless_mistake",
            str(val_a): "careless_mistake",
            str(m - n): "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Find scale factor = {val_a} / {m} = {k}.\n"
            f"Step 2: Difference in parts = {m} - {n} = {m - n}.\n"
            f"Step 3: Difference in people = {m - n} * {k} = {diff}."
        )

    else:  # three_way_one_known
        a, b, c = random.choice([(2, 3, 5), (3, 4, 6), (2, 5, 7), (1, 4, 7)])
        k = random.randint(6, 20)
        val_b = b * k
        total = (a + b + c) * k
        question = (
            f"The recipe for a baking mix requires flour, sugar, and cocoa in the ratio {a}:{b}:{c} by weight. "
            f"If {val_b} grams of sugar are used, what is the total weight of the baking mix?"
        )
        correct = f"{total} grams"
        distractors = [f"{a * k} grams", f"{c * k} grams", f"{(a + c) * k} grams"]
        trap_map = {
            f"{a * k} grams": "careless_mistake",
            f"{c * k} grams": "careless_mistake",
            f"{(a + c) * k} grams": "setup_mistake",
        }
        explanation = (
            f"Step 1: Sugar corresponds to {b} parts. Scale factor = {val_b} / {b} = {k} grams per part.\n"
            f"Step 2: Total parts in recipe = {a} + {b} + {c} = {a + b + c}.\n"
            f"Step 3: Total weight = ({a + b + c}) * {k} = {total} grams."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="ratio_one_value_known",
        subvariant=subvariant,
    )

