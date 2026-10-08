from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_ratio_variables_x_method(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "linear_relation_x",
        "difference_given_x",
        "sum_of_squares_x",
        "product_given_x",
        "consecutive_ratio_equations",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "difference_given_x":
        m = random.randint(5, 9)
        n = random.randint(2, m - 1)
        while gcd(m, n) != 1:
            n = random.randint(2, m - 1)
        x = random.randint(4, 15)
        diff = (m - n) * x
        ans_sum = (m + n) * x
        question = (
            f"Two positive integers are in the ratio {m}:{n}. "
            f"If the difference between them is {diff}, what is their sum?"
        )
        correct = str(ans_sum)
        distractors = [str(m * x), str(n * x), str(x)]
        trap_map = {
            str(m * x): "careless_mistake",
            str(n * x): "careless_mistake",
            str(x): "ratio_interpretation_mistake",
        }
        explanation = (
            f"Step 1: Represent the numbers as {m}x and {n}x.\n"
            f"Step 2: Their difference is {m}x - {n}x = {m - n}x = {diff}.\n"
            f"Step 3: Solve for x: x = {diff} / {m - n} = {x}.\n"
            f"Step 4: Their sum is ({m} + {n}) * {x} = {ans_sum}."
        )

    elif subvariant == "sum_of_squares_x":
        m, n = random.choice([(3, 4), (1, 2), (2, 3), (1, 3)])
        x = random.randint(2, 6)
        sum_sq = (m * m + n * n) * (x * x)
        ans_sum = (m + n) * x
        question = (
            f"Two positive numbers are in the ratio {m}:{n}. "
            f"If the sum of their squares is {sum_sq}, what is the sum of the two numbers?"
        )
        correct = str(ans_sum)
        distractors = [str(x), str(max(m, n) * x), str(sum_sq // (m + n))]
        trap_map = {
            str(x): "setup_mistake",
            str(max(m, n) * x): "careless_mistake",
            str(sum_sq // (m + n)): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Let the numbers be {m}x and {n}x.\n"
            f"Step 2: Sum of squares = ({m}x)^2 + ({n}x)^2 = {m*m}x^2 + {n*n}x^2 = {m*m + n*n}x^2.\n"
            f"Step 3: {m*m + n*n}x^2 = {sum_sq} => x^2 = {x*x} => x = {x}.\n"
            f"Step 4: Sum of the numbers = ({m} + {n}) * {x} = {ans_sum}."
        )

    elif subvariant == "product_given_x":
        m = random.randint(2, 5)
        n = random.randint(3, 7)
        while gcd(m, n) != 1:
            n = random.randint(3, 7)
        x = random.randint(3, 8)
        prod = m * n * (x * x)
        smaller = min(m, n) * x
        question = (
            f"The product of two positive numbers in the ratio {m}:{n} is {prod}. "
            f"What is the value of the smaller number?"
        )
        correct = str(smaller)
        larger = max(m, n) * x
        distractors = [str(larger), str(x), str(prod // (m * n))]
        trap_map = {
            str(larger): "careless_mistake",
            str(x): "setup_mistake",
            str(prod // (m * n)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Let the numbers be {m}x and {n}x.\n"
            f"Step 2: Product = ({m}x) * ({n}x) = {m * n}x^2 = {prod}.\n"
            f"Step 3: x^2 = {prod} / {m * n} = {x * x} => x = {x}.\n"
            f"Step 4: The smaller number is {min(m, n)} * {x} = {smaller}."
        )

    elif subvariant == "consecutive_ratio_equations":
        # A:B = m:n, B:C = p:q -> combine to A:B:C
        m, n = random.choice([(2, 3), (3, 4), (1, 2)])
        p, q = random.choice([(2, 5), (3, 5), (4, 3)])
        # B common = n * p
        term_a = m * p
        term_b = n * p
        term_c = n * q
        g = gcd(gcd(term_a, term_b), term_c)
        sa, sb, sc = term_a // g, term_b // g, term_c // g
        k = random.randint(4, 12)
        total = (sa + sb + sc) * k
        ans_b = sb * k
        question = (
            f"Three quantities A, B, and C satisfy A:B = {m}:{n} and B:C = {p}:{q}. "
            f"If A + B + C = {total}, what is the value of B?"
        )
        correct = str(ans_b)
        distractors = [str(sa * k), str(sc * k), str(total // 3)]
        trap_map = {
            str(sa * k): "careless_mistake",
            str(sc * k): "careless_mistake",
            str(total // 3): "average_weighted_mistake",
        }
        explanation = (
            f"Step 1: Combine the two ratios by finding a common multiple for B: B = {n} * {p} = {term_b}.\n"
            f"Step 2: A:B:C = ({m}*{p}) : ({n}*{p}) : ({n}*{q}) = {term_a}:{term_b}:{term_c}"
            + (f" = {sa}:{sb}:{sc}." if g > 1 else ".")
            + f"\nStep 3: Sum of parts = {sa + sb + sc}.\n"
            f"Step 4: Scale factor = {total} / {sa + sb + sc} = {k}.\n"
            f"Step 5: B = {sb} * {k} = {ans_b}."
        )

    else:  # linear_relation_x
        # Two numbers in ratio 3:4. If 5 is added to first and 5 subtracted from second, ratio is 4:3.
        # Or general setup
        m, n = 3, 5
        x = 6
        a_add = 7
        b_sub = 5
        # (3*6 + 7) = 25; (5*6 - 5) = 25 -> ratio 1:1
        question = (
            f"Two numbers are in the ratio {m}:{n}. "
            f"If {a_add} is added to the first number and {b_sub} is subtracted from the second number, "
            f"the two resulting numbers become equal. What is the sum of the two original numbers?"
        )
        # 3x + 7 = 5x - 5 => 2x = 12 => x = 6. Original sum = (3+5)*6 = 48.
        orig_sum = (m + n) * x
        correct = str(orig_sum)
        distractors = [str(x), str(m * x), str(n * x)]
        trap_map = {
            str(x): "setup_mistake",
            str(m * x): "careless_mistake",
            str(n * x): "careless_mistake",
        }
        explanation = (
            f"Step 1: Let the numbers be {m}x and {n}x.\n"
            f"Step 2: According to the problem: {m}x + {a_add} = {n}x - {b_sub}.\n"
            f"Step 3: {n - m}x = {a_add + b_sub} => {n - m}x = {a_add + b_sub} => x = {x}.\n"
            f"Step 4: Sum of the two original numbers = ({m} + {n}) * {x} = {orig_sum}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="ratio_variables_x_method",
        subvariant=subvariant,
    )

