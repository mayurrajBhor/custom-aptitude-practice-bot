from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_ratio_basics(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "interpret_ratio",
        "simplify_ratio",
        "equivalent_ratios",
        "compare_ratios",
        "convert_to_actual",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "interpret_ratio":
        if level <= 2:
            m = random.randint(2, 5)
            n = random.randint(3, 7)
            while gcd(m, n) != 1:
                n = random.randint(3, 7)
            tot = m + n
            question = (
                f"In a certain class, the ratio of boys to girls is {m}:{n}. "
                f"What fraction of the total students in the class are girls?"
            )
            correct = f"{n}/{tot}"
            distractors = [f"{m}/{tot}", f"{n}/{m}", f"{m}/{n}"]
            trap_map = {
                f"{m}/{tot}": "careless_mistake",
                f"{n}/{m}": "ratio_interpretation_mistake",
                f"{m}/{n}": "setup_mistake",
            }
            explanation = (
                f"Step 1: The ratio of boys to girls is {m}:{n}.\n"
                f"Step 2: Total proportional parts = {m} + {n} = {tot}.\n"
                f"Step 3: Girls represent {n} parts out of {tot}, so the fraction of girls is {n}/{tot}."
            )
        elif level <= 4:
            a, b, c = random.choice([(2, 3, 5), (3, 4, 5), (1, 3, 6), (2, 5, 7)])
            tot = a + b + c
            question = (
                f"A florist makes a bouquet containing red, white, and yellow roses in the ratio {a}:{b}:{c}. "
                f"What fraction of the total roses are white roses?"
            )
            frac = Fraction(b, tot)
            correct = f"{frac.numerator}/{frac.denominator}"
            distractors = [f"{b}/{a + c}", f"{a}/{tot}", f"{c}/{tot}"]
            trap_map = {
                f"{b}/{a + c}": "ratio_interpretation_mistake",
                f"{a}/{tot}": "careless_mistake",
                f"{c}/{tot}": "careless_mistake",
            }
            explanation = (
                f"Step 1: Total parts = {a} + {b} + {c} = {tot}.\n"
                f"Step 2: White roses account for {b} parts.\n"
                f"Step 3: The fraction is {b}/{tot}"
                + (f" = {correct}." if correct != f"{b}/{tot}" else ".")
            )
        else:
            m, n, pct = random.choice([
                (1, 3, "75%"),
                (3, 5, "62.5%"),
                (1, 4, "80%"),
                (2, 3, "60%"),
                (3, 7, "70%"),
            ])
            question = (
                f"In a technology firm, the ratio of software developers to product managers is {m}:{n}. "
                f"What percentage of the firm's total employees in these two roles are product managers?"
            )
            correct = pct
            pct_other = f"{(m / (m + n)) * 100:.1f}%".rstrip("0").rstrip(".") + "%"
            pct_ratio = f"{(n / m) * 100:.1f}%".rstrip("0").rstrip(".") + "%"
            distractors = [pct_other, pct_ratio, f"{n * 10}%"]
            trap_map = {
                pct_other: "careless_mistake",
                pct_ratio: "ratio_interpretation_mistake",
                f"{n * 10}%": "conceptual_mistake",
            }
            explanation = (
                f"Step 1: The total parts = {m} + {n} = {m + n}.\n"
                f"Step 2: Product managers comprise {n} parts out of {m + n}.\n"
                f"Step 3: Percentage = ({n} / {m + n}) * 100% = {correct}."
            )

    elif subvariant == "simplify_ratio":
        if level <= 2:
            a, b = random.choice([(2, 3), (3, 4), (3, 5), (4, 5), (5, 7)])
            k = random.randint(4, 12)
            val1, val2 = k * a, k * b
            question = f"Simplify the ratio {val1}:{val2} to its lowest integer terms."
            correct = f"{a}:{b}"
            distractors = [f"{b}:{a}", f"{a * 2}:{b * 2}", f"{a}:{b + 1}"]
            trap_map = {
                f"{b}:{a}": "careless_mistake",
                f"{a * 2}:{b * 2}": "arithmetic_mistake",
                f"{a}:{b + 1}": "arithmetic_mistake",
            }
            explanation = (
                f"Step 1: Identify the greatest common divisor of {val1} and {val2}, which is {k}.\n"
                f"Step 2: Divide both terms by {k}: {val1}/{k} = {a}, and {val2}/{k} = {b}.\n"
                f"Step 3: In lowest terms, the ratio is {correct}."
            )
        elif level <= 4:
            # Fraction ratio: a/b : c/d
            a, b, c, d = random.choice([(2, 3, 3, 4), (3, 5, 2, 3), (4, 7, 2, 5), (5, 6, 3, 4)])
            num1 = a * d
            num2 = b * c
            g = gcd(num1, num2)
            simp1, simp2 = num1 // g, num2 // g
            question = f"Express the ratio ({a}/{b}) : ({c}/{d}) in simplest integer form."
            correct = f"{simp1}:{simp2}"
            distractors = [f"{simp2}:{simp1}", f"{a * c}:{b * d}", f"{num1}:{num2 + g}"]
            trap_map = {
                f"{simp2}:{simp1}": "careless_mistake",
                f"{a * c}:{b * d}": "formula_selection_mistake",
                f"{num1}:{num2 + g}": "arithmetic_mistake",
            }
            explanation = (
                f"Step 1: Multiply both fractions by the common denominator {b * d}:\n"
                f"   ({a}/{b}) * {b * d} = {num1}\n"
                f"   ({c}/{d}) * {b * d} = {num2}\n"
                f"Step 2: Simplify {num1}:{num2} by dividing by gcd({num1}, {num2}) = {g}.\n"
                f"Step 3: The ratio in simplest integer form is {correct}."
            )
        else:
            # Units conversion ratio
            cm, m_val = random.choice([(75, 1.5), (40, 2.0), (80, 2.4), (250, 1.0)])
            cm_equiv = int(m_val * 100)
            g = gcd(cm, cm_equiv)
            r1, r2 = cm // g, cm_equiv // g
            question = f"Express the ratio of {cm} cm to {m_val} meters in simplest form."
            correct = f"{r1}:{r2}"
            distractors = [f"{r2}:{r1}", f"{cm}:{int(m_val)}", f"{r1}:{r2 * 2}"]
            trap_map = {
                f"{r2}:{r1}": "careless_mistake",
                f"{cm}:{int(m_val)}": "conceptual_mistake",
                f"{r1}:{r2 * 2}": "arithmetic_mistake",
            }
            explanation = (
                f"Step 1: Convert both measurements to the same units: {m_val} meters = {cm_equiv} cm.\n"
                f"Step 2: Form the ratio: {cm} : {cm_equiv}.\n"
                f"Step 3: Divide by gcd({cm}, {cm_equiv}) = {g} to obtain {correct}."
            )

    elif subvariant == "equivalent_ratios":
        if level <= 3:
            a = random.randint(2, 6)
            b = random.randint(3, 8)
            while gcd(a, b) != 1:
                b = random.randint(3, 8)
            k = random.randint(3, 9)
            c = a * k
            x = b * k
            question = f"If the ratio {a}:{b} is equivalent to {c}:x, what is the value of x?"
            correct = str(x)
            distractors = [str(x + k), str(x - a), str(a * k)]
            trap_map = {
                str(x + k): "arithmetic_mistake",
                str(x - a): "arithmetic_mistake",
                str(a * k): "careless_mistake",
            }
            explanation = (
                f"Step 1: An equivalent ratio means {a}/{b} = {c}/x.\n"
                f"Step 2: The scale factor from {a} to {c} is {c} / {a} = {k}.\n"
                f"Step 3: Multiply the second term by the scale factor: x = {b} * {k} = {x}."
            )
        else:
            # Algebraic equivalence: (2x + 1) : (3x + 2) = a : b
            x_val = random.randint(2, 6)
            val1 = 2 * x_val + 3
            val2 = 3 * x_val + 1
            g = gcd(val1, val2)
            a, b = val1 // g, val2 // g
            question = f"If (2x + 3) : (3x + 1) = {a} : {b}, what is the value of x?"
            correct = str(x_val)
            distractors = [str(x_val + 1), str(max(1, x_val - 1)), str(2 * x_val)]
            trap_map = {
                str(x_val + 1): "arithmetic_mistake",
                str(max(1, x_val - 1)): "setup_mistake",
                str(2 * x_val): "careless_mistake",
            }
            explanation = (
                f"Step 1: Cross-multiply: {b} * (2x + 3) = {a} * (3x + 1).\n"
                f"Step 2: Expand both sides: {2 * b}x + {3 * b} = {3 * a}x + {a}.\n"
                f"Step 3: Rearrange: ({3 * a - 2 * b})x = {3 * b - a}.\n"
                f"Step 4: Solve for x = {x_val}."
            )

    elif subvariant == "compare_ratios":
        if level <= 3:
            # Comparing two ratios: 3/5 vs 5/8
            ratios = [(3, 5), (5, 8), (4, 7), (2, 3)]
            random.shuffle(ratios)
            best_idx = 0
            best_val = ratios[0][0] / ratios[0][1]
            for i in range(1, 4):
                val = ratios[i][0] / ratios[i][1]
                if val > best_val:
                    best_val = val
                    best_idx = i
            correct = f"{ratios[best_idx][0]}:{ratios[best_idx][1]}"
            question = (
                f"Which of the following ratios has the greatest numerical value?\n"
                f"Choices: {ratios[0][0]}:{ratios[0][1]}, {ratios[1][0]}:{ratios[1][1]}, "
                f"{ratios[2][0]}:{ratios[2][1]}, {ratios[3][0]}:{ratios[3][1]}"
            )
            distractors = [f"{r[0]}:{r[1]}" for i, r in enumerate(ratios) if i != best_idx]
            trap_map = {d: "arithmetic_mistake" for d in distractors}
            explanation = (
                f"Step 1: Convert each ratio to decimal form:\n"
                + "\n".join([f"   {r[0]}:{r[1]} = {r[0]/r[1]:.4f}" for r in ratios])
                + f"\nStep 2: The largest decimal is {best_val:.4f}, which corresponds to {correct}."
            )
        else:
            # Conceptual: Adding positive constant to proper fraction
            question = (
                "If 0 < a < b and k is a positive constant, how does the ratio "
                "(a + k) : (b + k) compare to the original ratio a : b?"
            )
            correct = "Strictly greater than a:b"
            distractors = [
                "Strictly less than a:b",
                "Equal to a:b",
                "Depends on whether k is an integer",
            ]
            trap_map = {
                "Strictly less than a:b": "conceptual_mistake",
                "Equal to a:b": "ratio_interpretation_mistake",
                "Depends on whether k is an integer": "conceptual_mistake",
            }
            explanation = (
                "Step 1: Consider the cross-multiplication comparison between (a + k)/(b + k) and a/b.\n"
                "Step 2: (a + k)*b - a*(b + k) = ab + kb - ab - ka = k*(b - a).\n"
                "Step 3: Since k > 0 and b > a, k*(b - a) > 0, which proves (a + k)/(b + k) > a/b.\n"
                "Adding a positive constant to both terms of a proper ratio pulls it closer to 1, increasing its value."
            )

    else:  # convert_to_actual
        if level <= 3:
            m = random.randint(2, 5)
            n = random.randint(3, 7)
            while gcd(m, n) != 1:
                n = random.randint(3, 7)
            k = random.randint(4, 12)
            tot = k * (m + n)
            ask_category = "boys" if random.choice([True, False]) else "girls"
            ans = k * m if ask_category == "boys" else k * n
            other = k * n if ask_category == "boys" else k * m
            question = (
                f"The ratio of boys to girls in a school club is {m}:{n}. "
                f"If there are {tot} students in the club in total, how many {ask_category} are in the club?"
            )
            correct = str(ans)
            distractors = [str(other), str(k), str(m if ask_category == "boys" else n)]
            trap_map = {
                str(other): "careless_mistake",
                str(k): "setup_mistake",
                str(m if ask_category == "boys" else n): "ratio_interpretation_mistake",
            }
            explanation = (
                f"Step 1: Total ratio units = {m} + {n} = {m + n}.\n"
                f"Step 2: Value per unit = {tot} / {m + n} = {k}.\n"
                f"Step 3: Number of {ask_category} = {k} * {m if ask_category == 'boys' else n} = {ans}."
            )
        else:
            # Level 4-5: Multi-step with item prices
            m, n = 3, 5
            tot_items = 64
            k = tot_items // (m + n)  # 8
            apples = m * k  # 24
            oranges = n * k  # 40
            p_apple = 0.75
            p_orange = 0.50
            total_cost = int(round(apples * p_apple + oranges * p_orange))  # 18 + 20 = 38
            question = (
                f"The ratio of apples to oranges in a crate is {m}:{n}, with {tot_items} fruits in total. "
                f"If each apple sells for $0.75 and each orange sells for $0.50, what is the total sales value of the crate?"
            )
            correct = f"${total_cost}"
            distractors = [f"${total_cost - 4}", f"${total_cost + 4}", f"${apples + oranges}"]
            trap_map = {
                f"${total_cost - 4}": "arithmetic_mistake",
                f"${total_cost + 4}": "setup_mistake",
                f"${apples + oranges}": "conceptual_mistake",
            }
            explanation = (
                f"Step 1: Ratio sum = {m} + {n} = {m + n}.\n"
                f"Step 2: Scale factor = {tot_items} / {m + n} = {k}.\n"
                f"Step 3: Apples = {m} * {k} = {apples}; Oranges = {n} * {k} = {oranges}.\n"
                f"Step 4: Total revenue = ({apples} * $0.75) + ({oranges} * $0.50) = $18 + $20 = ${total_cost}."
            )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="ratio_basics",
        subvariant=subvariant,
    )

