from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_proportion(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "fourth_proportional",
        "mean_proportional",
        "third_proportional",
        "cross_multiplication_algebra",
        "scale_factor_proportion",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "fourth_proportional":
        # a : b = c : x => x = (b * c) / a
        a = random.choice([3, 4, 5, 6, 7])
        mult = random.randint(2, 6)
        c = a * mult
        b = random.randint(4, 15)
        x = b * mult
        question = f"What is the fourth proportional to {a}, {b}, and {c}?"
        correct = str(x)
        distractors = [str((a * c) // b if b != 0 else x + 2), str((a * b) // c if c != 0 else x - 2), str(x + mult)]
        trap_map = {
            distractors[0]: "setup_mistake",
            distractors[1]: "setup_mistake",
            distractors[2]: "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: By definition of fourth proportional, {a} / {b} = {c} / x.\n"
            f"Step 2: Cross-multiply: {a} * x = {b} * {c}.\n"
            f"Step 3: x = ({b} * {c}) / {a} = ({b} * {c}) / {a} = {x}."
        )

    elif subvariant == "mean_proportional":
        # Mean proportional between a and b: x = sqrt(a * b)
        pairs = [(4, 16, 8), (9, 25, 15), (8, 18, 12), (12, 27, 18), (16, 36, 24), (9, 49, 21)]
        a, b, x = random.choice(pairs)
        arith_mean = (a + b) // 2
        question = f"Find the mean proportional between {a} and {b}."
        correct = str(x)
        distractors = [str(arith_mean), str(a * b), str(2 * x)]
        trap_map = {
            str(arith_mean): "formula_selection_mistake",
            str(a * b): "arithmetic_mistake",
            str(2 * x): "setup_mistake",
        }
        explanation = (
            f"Step 1: The mean proportional x between a and b satisfies a / x = x / b, so x^2 = a * b.\n"
            f"Step 2: x^2 = {a} * {b} = {a * b}.\n"
            f"Step 3: x = sqrt({a * b}) = {x}."
        )

    elif subvariant == "third_proportional":
        # a : b = b : x => x = b^2 / a
        pairs = [(4, 12, 36), (9, 18, 36), (8, 24, 72), (6, 18, 54), (16, 24, 36), (12, 36, 108)]
        a, b, x = random.choice(pairs)
        question = f"Find the third proportional to {a} and {b}."
        correct = str(x)
        distractors = [str(b * 2), str(b // a if a != 0 else 1), str(int(math.isqrt(a * b)))]
        trap_map = {
            str(b * 2): "arithmetic_mistake",
            str(b // a if a != 0 else 1): "setup_mistake",
            str(int(math.isqrt(a * b))): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: The third proportional x to a and b satisfies {a} : {b} = {b} : x.\n"
            f"Step 2: {a}x = {b}^2 = {b * b}.\n"
            f"Step 3: x = {b * b} / {a} = {x}."
        )

    elif subvariant == "cross_multiplication_algebra":
        # (2x + 5)/(3x + 1) = 3/4
        # 4(2x + 5) = 3(3x + 1) => 8x + 20 = 9x + 3 => x = 17
        x_val = random.randint(3, 9)
        c1, c2 = 2, 3
        d1 = random.randint(1, 5)
        num = c1 * x_val + d1
        # choose c2, d2 so denom is coprime or clean
        den = c2 * x_val - 2
        g = gcd(num, den)
        p, q = num // g, den // g
        question = f"Solve for x: ({c1}x + {d1}) / ({c2}x - 2) = {p} / {q}."
        correct = str(x_val)
        distractors = [str(x_val + 2), str(max(1, x_val - 2)), str(x_val * 2)]
        trap_map = {
            str(x_val + 2): "arithmetic_mistake",
            str(max(1, x_val - 2)): "sign_mistake",
            str(x_val * 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Cross-multiply: {q}({c1}x + {d1}) = {p}({c2}x - 2).\n"
            f"Step 2: Expand: {q * c1}x + {q * d1} = {p * c2}x - {p * 2}.\n"
            f"Step 3: Collect terms in x: ({p * c2 - q * c1})x = {q * d1 + p * 2}.\n"
            f"Step 4: Solve for x = {x_val}."
        )

    else:  # scale_factor_proportion
        scale_km = random.choice([25, 40, 50, 75, 100])
        map_cm = random.choice([3, 4, 5, 6, 8])
        actual_dist = map_cm * scale_km
        question = (
            f"On a certain map, 1 centimeter represents an actual ground distance of {scale_km} kilometers. "
            f"If the distance between two cities on the map is {map_cm} centimeters, what is the actual distance between them?"
        )
        correct = f"{actual_dist} km"
        distractors = [f"{scale_km // map_cm} km", f"{actual_dist + scale_km} km", f"{map_cm * 10} km"]
        trap_map = {
            f"{scale_km // map_cm} km": "formula_selection_mistake",
            f"{actual_dist + scale_km} km": "arithmetic_mistake",
            f"{map_cm * 10} km": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Use the direct scale proportion: Actual Distance = Map Distance * Scale Factor.\n"
            f"Step 2: Actual Distance = {map_cm} cm * {scale_km} km/cm = {actual_dist} km."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="proportion",
        subvariant=subvariant,
    )

