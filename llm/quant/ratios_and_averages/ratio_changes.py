from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_ratio_changes(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "add_to_one_part",
        "remove_from_one_part",
        "ratio_becomes_equal",
        "add_to_both_parts",
        "remove_from_both_parts",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "add_to_one_part":
        # Ratio A:B is m:n. Add k units of B -> new ratio m:n2 (A stays mx)
        m = random.choice([2, 3, 4, 5])
        n = random.randint(2, 5)
        n2 = n + random.randint(2, 4)
        x = random.randint(3, 10)
        added_b = (n2 - n) * x
        orig_a = m * x
        question = (
            f"A container holds a mixture of orange juice and water in the ratio {m}:{n}. "
            f"When {added_b} liters of water are added, the ratio becomes {m}:{n2}. "
            f"How many liters of orange juice are in the container?"
        )
        correct = f"{orig_a} liters"
        distractors = [f"{n * x} liters", f"{x} liters", f"{m * n2} liters"]
        trap_map = {
            f"{n * x} liters": "careless_mistake",
            f"{x} liters": "setup_mistake",
            f"{m * n2} liters": "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: The amount of orange juice does not change and remains {m}x.\n"
            f"Step 2: Water increases from {n}x to {n2}x, so the added water is ({n2} - {n})x = {n2 - n}x.\n"
            f"Step 3: {n2 - n}x = {added_b} => x = {x}.\n"
            f"Step 4: Orange juice = {m} * {x} = {orig_a} liters."
        )

    elif subvariant == "remove_from_one_part":
        # Ratio A:B is m:n. Remove k units of A -> new ratio m2:n (B stays nx)
        n = random.choice([2, 3, 4])
        m2 = random.randint(2, 4)
        m = m2 + random.randint(2, 4)
        x = random.randint(4, 12)
        removed_a = (m - m2) * x
        orig_a = m * x
        question = (
            f"The ratio of red counters to blue counters in a box is {m}:{n}. "
            f"If {removed_a} red counters are removed, the new ratio of red to blue counters is {m2}:{n}. "
            f"What was the original number of red counters in the box?"
        )
        correct = str(orig_a)
        distractors = [str(m2 * x), str(n * x), str(x)]
        trap_map = {
            str(m2 * x): "careless_mistake",
            str(n * x): "careless_mistake",
            str(x): "setup_mistake",
        }
        explanation = (
            f"Step 1: The number of blue counters is unchanged at {n}x.\n"
            f"Step 2: Red counters decreased from {m}x to {m2}x, a drop of ({m} - {m2})x = {m - m2}x.\n"
            f"Step 3: {m - m2}x = {removed_a} => x = {x}.\n"
            f"Step 4: Original red counters = {m} * {x} = {orig_a}."
        )

    elif subvariant == "ratio_becomes_equal":
        # A:B = m:n (m > n). Transfer t from A to B so they become 1:1.
        m = random.choice([5, 7, 9])
        n = random.choice([1, 3])
        x = random.randint(4, 12)
        val_a = m * x
        val_b = n * x
        transfer = (val_a - val_b) // 2
        question = (
            f"Box A has {val_a} tokens and Box B has {val_b} tokens, so the ratio of tokens in Box A to Box B is {m}:{n}. "
            f"How many tokens must be transferred from Box A to Box B so that both boxes have an equal number of tokens?"
        )
        correct = str(transfer)
        distractors = [str(val_a - val_b), str((val_a + val_b) // 2), str(m - n)]
        trap_map = {
            str(val_a - val_b): "conceptual_mistake",
            str((val_a + val_b) // 2): "formula_selection_mistake",
            str(m - n): "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Let t be the number of tokens transferred.\n"
            f"Step 2: After transfer, Box A has {val_a} - t and Box B has {val_b} + t.\n"
            f"Step 3: For them to be equal: {val_a} - t = {val_b} + t => 2t = {val_a} - {val_b} = {val_a - val_b}.\n"
            f"Step 4: t = {val_a - val_b} / 2 = {transfer} tokens."
        )

    elif subvariant == "add_to_both_parts":
        # (mx + k)/(nx + k) = p/q.
        # Pick m=2, n=3, x=5 -> 10, 15. Add k=5 -> 15, 20 -> 3:4.
        # Pick m=3, n=5, x=4 -> 12, 20. Add k=4 -> 16, 24 -> 2:3.
        m, n, p, q, k, x = random.choice([
            (2, 3, 3, 4, 5, 5),
            (3, 5, 2, 3, 4, 4),
            (1, 2, 2, 3, 6, 6),
            (4, 5, 5, 6, 3, 3),
        ])
        orig_sum = (m + n) * x
        question = (
            f"The ratio of two positive numbers is {m}:{n}. "
            f"If {k} is added to each number, the new ratio becomes {p}:{q}. "
            f"What is the sum of the two original numbers?"
        )
        correct = str(orig_sum)
        distractors = [str(orig_sum + 2 * k), str(m * x), str(n * x)]
        trap_map = {
            str(orig_sum + 2 * k): "careless_mistake",
            str(m * x): "setup_mistake",
            str(n * x): "setup_mistake",
        }
        explanation = (
            f"Step 1: Let the two numbers be {m}x and {n}x.\n"
            f"Step 2: Set up the equation: ({m}x + {k}) / ({n}x + {k}) = {p} / {q}.\n"
            f"Step 3: Cross-multiply: {q}({m}x + {k}) = {p}({n}x + {k}) => {q * m}x + {q * k} = {p * n}x + {p * k}.\n"
            f"Step 4: Solve for x: ({p * n - q * m})x = {q * k - p * k} => x = {x}.\n"
            f"Step 5: Sum of original numbers = ({m} + {n}) * {x} = {orig_sum}."
        )

    else:  # remove_from_both_parts
        # (mx - k)/(nx - k) = p/q
        m, n, p, q, k, x = random.choice([
            (3, 4, 2, 3, 6, 6),
            (5, 7, 3, 5, 4, 4),
            (4, 5, 3, 4, 5, 5),
            (5, 6, 4, 5, 8, 8),
        ])
        larger = max(m, n) * x
        question = (
            f"Two numbers are in the ratio {m}:{n}. "
            f"If {k} is subtracted from each number, the ratio becomes {p}:{q}. "
            f"What is the value of the larger original number?"
        )
        correct = str(larger)
        smaller = min(m, n) * x
        distractors = [str(smaller), str((m + n) * x), str(x)]
        trap_map = {
            str(smaller): "careless_mistake",
            str((m + n) * x): "setup_mistake",
            str(x): "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Let the numbers be {m}x and {n}x.\n"
            f"Step 2: ({m}x - {k}) / ({n}x - {k}) = {p} / {q}.\n"
            f"Step 3: Cross-multiply: {q}({m}x - {k}) = {p}({n}x - {k}) => x = {x}.\n"
            f"Step 4: The larger number is {max(m, n)} * {x} = {larger}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="ratio_changes",
        subvariant=subvariant,
    )

