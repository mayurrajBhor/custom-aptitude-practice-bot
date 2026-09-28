"""Day 4 GMAT Practice Engine: Ratios, Proportions, and Averages.

This module implements question generators for Patterns 5040 through 5055:
- Pattern 5040: ratio_basics
- Pattern 5041: ratio_with_total
- Pattern 5042: ratio_one_value_known
- Pattern 5043: ratio_changes
- Pattern 5044: ratio_variables_x_method
- Pattern 5045: proportion
- Pattern 5046: direct_proportion
- Pattern 5047: inverse_proportion
- Pattern 5048: average_basics
- Pattern 5049: missing_number_average
- Pattern 5050: adding_number_to_average
- Pattern 5051: removing_number_from_average
- Pattern 5052: average_change_shortcut
- Pattern 5053: weighted_average
- Pattern 5054: weighted_average_intuition
- Pattern 5055: gmat_mixed_questions
"""

import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional

from llm.gmat.common import clamp_level, gcd, make_mcq


# -----------------------------------------------------------------------------
# Pattern 5040: Ratio Basics
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5041: Ratio With Total
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5042: Ratio One Value Known
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5043: Ratio Changes
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5044: Ratio Variables (x-Method)
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5045: Proportion
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# Pattern 5046: Direct Proportion
# -----------------------------------------------------------------------------
def generate_direct_proportion(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "items_and_cost",
        "distance_and_fuel",
        "hours_and_production",
        "weight_and_price",
        "speed_constant_time",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "items_and_cost":
        unit_cost = random.randint(4, 18)
        n1 = random.randint(3, 8)
        c1 = n1 * unit_cost
        n2 = random.randint(9, 20)
        c2 = n2 * unit_cost
        question = (
            f"If {n1} identical notebooks cost a total of ${c1}, "
            f"what is the cost of {n2} of these notebooks?"
        )
        correct = f"${c2}"
        distractors = [f"${c2 - unit_cost}", f"${c2 + unit_cost}", f"${int((n1 * c1) / n2)}"]
        trap_map = {
            f"${c2 - unit_cost}": "arithmetic_mistake",
            f"${c2 + unit_cost}": "arithmetic_mistake",
            f"${int((n1 * c1) / n2)}": "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Find unit cost: ${c1} / {n1} = ${unit_cost} per notebook.\n"
            f"Step 2: Multiply by new quantity: {n2} * ${unit_cost} = ${c2}."
        )

    elif subvariant == "distance_and_fuel":
        km_per_liter = random.choice([12, 14, 15, 16, 18])
        f1 = random.randint(3, 6)
        d1 = f1 * km_per_liter
        f2 = random.randint(7, 15)
        d2 = f2 * km_per_liter
        question = (
            f"A car travels {d1} kilometers on {f1} liters of petrol. "
            f"Assuming the consumption rate remains constant, how many kilometers can it travel on {f2} liters?"
        )
        correct = f"{d2} km"
        distractors = [f"{d2 - km_per_liter} km", f"{d2 + km_per_liter} km", f"{int(d1 * f1 / f2)} km"]
        trap_map = {
            f"{d2 - km_per_liter} km": "arithmetic_mistake",
            f"{d2 + km_per_liter} km": "arithmetic_mistake",
            f"{int(d1 * f1 / f2)} km": "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Calculate fuel economy: {d1} km / {f1} L = {km_per_liter} km/L.\n"
            f"Step 2: Distance on {f2} liters = {f2} * {km_per_liter} = {d2} km."
        )

    elif subvariant == "hours_and_production":
        rate = random.randint(25, 60)
        h1 = random.randint(2, 5)
        p1 = h1 * rate
        h2 = h1 + random.randint(3, 6)
        p2 = h2 * rate
        question = (
            f"An automated packaging machine produces {p1} packages in {h1} hours. "
            f"At this consistent rate, how many packages will it produce in {h2} hours?"
        )
        correct = str(p2)
        distractors = [str(p2 - rate), str(p2 + rate), str(int(p1 * h1 / h2))]
        trap_map = {
            str(p2 - rate): "arithmetic_mistake",
            str(p2 + rate): "arithmetic_mistake",
            str(int(p1 * h1 / h2)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Production rate = {p1} packages / {h1} hours = {rate} packages/hour.\n"
            f"Step 2: Output in {h2} hours = {h2} * {rate} = {p2} packages."
        )

    elif subvariant == "weight_and_price":
        price_per_kg = random.randint(15, 45)
        w1 = random.choice([2, 4, 5])
        c1 = w1 * price_per_kg
        w2 = w1 + random.choice([3, 5, 7])
        c2 = w2 * price_per_kg
        question = (
            f"The cost of copper cable is directly proportional to its weight. "
            f"If a roll weighing {w1} kg costs ${c1}, how much does a roll weighing {w2} kg cost?"
        )
        correct = f"${c2}"
        distractors = [f"${c2 - price_per_kg}", f"${c2 + price_per_kg}", f"${c1 + w2}"]
        trap_map = {
            f"${c2 - price_per_kg}": "arithmetic_mistake",
            f"${c2 + price_per_kg}": "arithmetic_mistake",
            f"${c1 + w2}": "setup_mistake",
        }
        explanation = (
            f"Step 1: Cost per kg = ${c1} / {w1} = ${price_per_kg} per kg.\n"
            f"Step 2: Cost for {w2} kg = {w2} * ${price_per_kg} = ${c2}."
        )

    else:  # speed_constant_time
        time_hrs = random.choice([2, 3, 4])
        s1 = random.choice([40, 50, 60])
        d1 = s1 * time_hrs
        s2 = s1 + random.choice([15, 20, 30])
        d2 = s2 * time_hrs
        question = (
            f"In a fixed duration of time, a train covers {d1} miles traveling at {s1} mph. "
            f"If the train increases its speed to {s2} mph, how many miles will it cover in the same duration?"
        )
        correct = f"{d2} miles"
        distractors = [f"{d1} miles", f"{int(d1 * s1 / s2)} miles", f"{d2 + 10} miles"]
        trap_map = {
            f"{d1} miles": "conceptual_mistake",
            f"{int(d1 * s1 / s2)} miles": "formula_selection_mistake",
            f"{d2 + 10} miles": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Time = Distance / Speed = {d1} / {s1} = {time_hrs} hours.\n"
            f"Step 2: Distance at {s2} mph = {time_hrs} * {s2} = {d2} miles."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="direct_proportion",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5047: Inverse Proportion
# -----------------------------------------------------------------------------
def generate_inverse_proportion(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "workers_and_days",
        "speed_and_time",
        "pipes_or_machines",
        "provisions_and_people",
        "gear_teeth_revolutions",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "workers_and_days":
        # w1 * d1 = w2 * d2
        w1 = random.choice([6, 8, 10, 12])
        d1 = random.choice([12, 15, 20, 24])
        total_work = w1 * d1
        # Pick w2 divisor of total_work
        factors = [f for f in range(3, total_work) if total_work % f == 0 and f != w1]
        w2 = random.choice(factors[:6])
        d2 = total_work // w2
        question = (
            f"{w1} workers can complete a construction job in {d1} days working at identical rates. "
            f"How many days will {w2} workers take to complete the same job?"
        )
        correct = f"{d2} days"
        wrong_direct = f"{int((w2 * d1) / w1)} days"
        distractors = [wrong_direct, f"{d2 + 2} days", f"{max(1, d2 - 2)} days"]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            f"{d2 + 2} days": "arithmetic_mistake",
            f"{max(1, d2 - 2)} days": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Workers and days are inversely proportional: Total Worker-Days = w1 * d1 = {w1} * {d1} = {total_work}.\n"
            f"Step 2: For {w2} workers: {w2} * d2 = {total_work}.\n"
            f"Step 3: d2 = {total_work} / {w2} = {d2} days."
        )

    elif subvariant == "speed_and_time":
        s1 = random.choice([40, 50, 60, 75])
        t1 = random.choice([3, 4, 5, 6])
        distance = s1 * t1
        factors = [f for f in range(2, 10) if distance % f == 0 and f != t1]
        t2 = random.choice(factors)
        s2 = distance // t2
        question = (
            f"A motorist traveling at an average speed of {s1} km/h completes a journey in {t1} hours. "
            f"What average speed must the motorist maintain to complete the same journey in {t2} hours?"
        )
        correct = f"{s2} km/h"
        wrong_direct = f"{int((s1 * t2) / t1)} km/h"
        distractors = [wrong_direct, f"{s2 + 5} km/h", f"{s2 - 5} km/h"]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            f"{s2 + 5} km/h": "arithmetic_mistake",
            f"{s2 - 5} km/h": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total distance = speed * time = {s1} km/h * {t1} hours = {distance} km.\n"
            f"Step 2: Required speed for {t2} hours = Distance / {t2} = {distance} / {t2} = {s2} km/h."
        )

    elif subvariant == "pipes_or_machines":
        m1 = random.choice([4, 6, 8])
        h1 = random.choice([6, 9, 12])
        total_machine_hours = m1 * h1
        factors = [f for f in range(2, 15) if total_machine_hours % f == 0 and f != h1]
        h2 = random.choice(factors)
        m2 = total_machine_hours // h2
        question = (
            f"{m1} identical industrial printing machines can finish a bulk printing order in {h1} hours. "
            f"How many of these machines are needed to complete the order in {h2} hours?"
        )
        correct = str(m2)
        wrong_direct = str(int((m1 * h2) / h1))
        distractors = [wrong_direct, str(m2 + 1), str(max(1, m2 - 1))]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            str(m2 + 1): "arithmetic_mistake",
            str(max(1, m2 - 1)): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total machine-hours required = {m1} * {h1} = {total_machine_hours}.\n"
            f"Step 2: Number of machines required = Total machine-hours / {h2} = {total_machine_hours} / {h2} = {m2}."
        )

    elif subvariant == "provisions_and_people":
        p1 = random.choice([30, 40, 50, 60])
        d1 = random.choice([20, 25, 30])
        tot_person_days = p1 * d1
        # Add people
        p_extra = random.choice([10, 20])
        p2 = p1 + p_extra
        d2 = tot_person_days // p2
        # adjust to exact division
        tot_person_days = p2 * d2
        d1 = tot_person_days // p1
        question = (
            f"A military post has sufficient food supplies for {p1} soldiers for {d1} days. "
            f"If {p_extra} additional soldiers join the post, how many days will the supplies last?"
        )
        correct = f"{d2} days"
        distractors = [f"{d1 - p_extra} days", f"{int(d1 * p2 / p1)} days", f"{d2 + 3} days"]
        trap_map = {
            f"{d1 - p_extra} days": "conceptual_mistake",
            f"{int(d1 * p2 / p1)} days": "formula_selection_mistake",
            f"{d2 + 3} days": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total rations = {p1} soldiers * {d1} days = {tot_person_days} person-days.\n"
            f"Step 2: New group size = {p1} + {p_extra} = {p2} soldiers.\n"
            f"Step 3: Days supplies will last = {tot_person_days} / {p2} = {d2} days."
        )

    else:  # gear_teeth_revolutions
        t1, r1, t2, r2 = random.choice([
            (20, 15, 30, 10),
            (24, 10, 40, 6),
            (16, 25, 40, 10),
            (18, 20, 24, 15),
        ])
        question = (
            f"Gear A has {t1} teeth and meshes with Gear B which has {t2} teeth. "
            f"When Gear A makes {r1} complete revolutions, how many revolutions does Gear B make?"
        )
        correct = str(r2)
        wrong_direct = str(int((t2 * r1) / t1))
        distractors = [wrong_direct, str(r2 + 2), str(max(1, r2 - 2))]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            str(r2 + 2): "arithmetic_mistake",
            str(max(1, r2 - 2)): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: The number of teeth passing the contact point is constant: teeth * revolutions = constant.\n"
            f"Step 2: {t1} * {r1} = {t1 * r1}.\n"
            f"Step 3: Gear B revolutions = ({t1} * {r1}) / {t2} = {t1 * r1} / {t2} = {r2} revolutions."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="inverse_proportion",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5048: Average Basics
# -----------------------------------------------------------------------------
def generate_average_basics(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "compute_average",
        "find_sum_from_average",
        "find_count_from_sum_and_avg",
        "average_of_consecutive_integers",
        "average_of_multiples",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "compute_average":
        n = random.randint(4, 6) if level <= 3 else random.randint(5, 7)
        avg = random.randint(15, 45)
        # Generate n numbers that average to avg
        diffs = [random.randint(-10, 10) for _ in range(n - 1)]
        diffs.append(-sum(diffs))
        nums = [avg + d for d in diffs]
        nums_str = ", ".join(map(str, nums))
        question = f"What is the arithmetic mean (average) of the following numbers: {nums_str}?"
        correct = str(avg)
        distractors = [str(avg + 2), str(avg - 2), str(sum(nums) // (n - 1))]
        trap_map = {
            str(avg + 2): "arithmetic_mistake",
            str(avg - 2): "arithmetic_mistake",
            str(sum(nums) // (n - 1)): "setup_mistake",
        }
        explanation = (
            f"Step 1: Sum the {n} numbers: {sum(nums)}.\n"
            f"Step 2: Divide the sum by the count of numbers ({n}): {sum(nums)} / {n} = {avg}."
        )

    elif subvariant == "find_sum_from_average":
        n = random.randint(5, 12)
        avg = random.randint(20, 60)
        tot = n * avg
        question = (
            f"A group of {n} students took a test, scoring an average of {avg} points. "
            f"What was the total sum of all their test scores?"
        )
        correct = str(tot)
        distractors = [str(tot + avg), str(tot - avg), str(int(tot / n))]
        trap_map = {
            str(tot + avg): "setup_mistake",
            str(tot - avg): "setup_mistake",
            str(int(tot / n)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the fundamental formula: Sum = Average * Count.\n"
            f"Step 2: Sum = {avg} * {n} = {tot}."
        )

    elif subvariant == "find_count_from_sum_and_avg":
        n = random.randint(6, 15)
        avg = random.randint(14, 35)
        tot = n * avg
        question = (
            f"A set of measurements has a total sum of {tot} and an average value of {avg}. "
            f"How many measurements are in the set?"
        )
        correct = str(n)
        distractors = [str(n + 1), str(n - 1), str(tot * avg)]
        trap_map = {
            str(n + 1): "arithmetic_mistake",
            str(n - 1): "arithmetic_mistake",
            str(tot * avg): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the relationship: Count = Sum / Average.\n"
            f"Step 2: Count = {tot} / {avg} = {n}."
        )

    elif subvariant == "average_of_consecutive_integers":
        start = random.randint(11, 40)
        k = random.choice([7, 9, 11, 15])  # odd number of integers
        end = start + k - 1
        avg = (start + end) // 2
        question = f"What is the average of all consecutive integers from {start} to {end}, inclusive?"
        correct = str(avg)
        distractors = [str(avg + 1), str(avg - 1), str(end - start)]
        trap_map = {
            str(avg + 1): "arithmetic_mistake",
            str(avg - 1): "arithmetic_mistake",
            str(end - start): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: For any evenly spaced sequence, Average = (First Term + Last Term) / 2.\n"
            f"Step 2: Average = ({start} + {end}) / 2 = {start + end} / 2 = {avg}."
        )

    else:  # average_of_multiples
        m = random.choice([3, 4, 5, 6, 7, 8])
        k = random.choice([7, 9, 11, 13])  # odd number of multiples
        avg = (m * (k + 1)) // 2
        question = f"What is the average of the first {k} positive multiples of {m}?"
        correct = str(avg)
        distractors = [str(avg + m), str(avg - m), str(m * k)]
        trap_map = {
            str(avg + m): "arithmetic_mistake",
            str(avg - m): "arithmetic_mistake",
            str(m * k): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: The first multiple is {m}*1 = {m}, and the {k}th multiple is {m}*{k} = {m * k}.\n"
            f"Step 2: Since multiples form an arithmetic progression, Average = (First + Last) / 2.\n"
            f"Step 3: Average = ({m} + {m * k}) / 2 = {m + m * k} / 2 = {avg}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="average_basics",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5049: Missing Number Average
# -----------------------------------------------------------------------------
def generate_missing_number_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "one_missing_in_set",
        "test_score_target",
        "consecutive_series_with_unknown",
        "two_missing_with_relation",
        "missing_sales_or_daily_target",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "one_missing_in_set":
        n = random.randint(4, 6)
        target_avg = random.randint(20, 50)
        total_sum = n * target_avg
        known_nums = [random.randint(target_avg - 15, target_avg + 15) for _ in range(n - 1)]
        missing = total_sum - sum(known_nums)
        nums_str = ", ".join(map(str, known_nums))
        question = (
            f"The average of a set of {n} numbers is {target_avg}. "
            f"If {n - 1} of the numbers are {nums_str}, what is the missing number?"
        )
        correct = str(missing)
        distractors = [str(missing + 2), str(missing - 2), str(target_avg)]
        trap_map = {
            str(missing + 2): "arithmetic_mistake",
            str(missing - 2): "arithmetic_mistake",
            str(target_avg): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total sum of all {n} numbers = {n} * {target_avg} = {total_sum}.\n"
            f"Step 2: Sum of known numbers = {sum(known_nums)}.\n"
            f"Step 3: Missing number = {total_sum} - {sum(known_nums)} = {missing}."
        )

    elif subvariant == "test_score_target":
        target = random.choice([80, 82, 85, 88, 90])
        # 4 test scores given, find 5th test score
        scores = [random.randint(target - 12, target + 8) for _ in range(4)]
        needed = 5 * target - sum(scores)
        scores_str = ", ".join(map(str, scores))
        question = (
            f"A student scores {scores_str} on four history tests. "
            f"What score must the student achieve on the fifth test to attain an overall average of {target}?"
        )
        correct = str(needed)
        distractors = [str(needed + 4), str(needed - 4), str(target)]
        trap_map = {
            str(needed + 4): "arithmetic_mistake",
            str(needed - 4): "arithmetic_mistake",
            str(target): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total points required across 5 tests = 5 * {target} = {5 * target}.\n"
            f"Step 2: Sum of first 4 scores = {sum(scores)}.\n"
            f"Step 3: Required 5th score = {5 * target} - {sum(scores)} = {needed}."
        )

    elif subvariant == "consecutive_series_with_unknown":
        k = random.choice([5, 7])
        avg = random.randint(25, 60)
        largest = avg + (k - 1) // 2
        smallest = avg - (k - 1) // 2
        ask_largest = random.choice([True, False])
        ans = largest if ask_largest else smallest
        term_type = "largest" if ask_largest else "smallest"
        question = (
            f"The average of {k} consecutive integers is {avg}. "
            f"What is the {term_type} of these integers?"
        )
        correct = str(ans)
        other = smallest if ask_largest else largest
        distractors = [str(other), str(avg), str(ans + 1)]
        trap_map = {
            str(other): "careless_mistake",
            str(avg): "setup_mistake",
            str(ans + 1): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: For {k} consecutive integers, the average is the exact middle integer = {avg}.\n"
            f"Step 2: The integers extend {(k - 1) // 2} steps to the left and to the right.\n"
            f"Step 3: The {term_type} integer is {avg} {'+' if ask_largest else '-'} {(k - 1) // 2} = {ans}."
        )

    elif subvariant == "two_missing_with_relation":
        n = 5
        avg = random.randint(30, 60)
        tot = n * avg
        known3 = [avg - 6, avg + 2, avg - 4]
        sum_known = sum(known3)
        rem_sum = tot - sum_known
        d = random.choice([4, 6, 8])
        larger = (rem_sum + d) // 2
        smaller = larger - d
        question = (
            f"The average of 5 numbers is {avg}. Three of the numbers are {known3[0]}, {known3[1]}, and {known3[2]}. "
            f"The remaining two numbers differ by {d}. What is the value of the larger of the two missing numbers?"
        )
        correct = str(larger)
        distractors = [str(smaller), str(rem_sum // 2), str(larger + d)]
        trap_map = {
            str(smaller): "careless_mistake",
            str(rem_sum // 2): "setup_mistake",
            str(larger + d): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total sum = 5 * {avg} = {tot}.\n"
            f"Step 2: Sum of known 3 numbers = {sum_known}.\n"
            f"Step 3: Sum of two missing numbers = {tot} - {sum_known} = {rem_sum}.\n"
            f"Step 4: If smaller is x, larger is x + {d}. 2x + {d} = {rem_sum} => x = {smaller}.\n"
            f"Step 5: The larger missing number is {smaller} + {d} = {larger}."
        )

    else:  # missing_sales_or_daily_target
        days = 6
        target_avg = random.choice([250, 300, 400])
        tot_target = days * target_avg
        sales = [random.randint(target_avg - 50, target_avg + 40) for _ in range(days - 1)]
        needed = tot_target - sum(sales)
        sales_str = ", ".join([f"${s}" for s in sales])
        question = (
            f"A retail shop targets an average daily revenue of ${target_avg} over a 6-day work week. "
            f"If revenues for Monday through Friday were {sales_str}, what must the revenue be on Saturday to reach the target?"
        )
        correct = f"${needed}"
        distractors = [f"${needed + 25}", f"${needed - 25}", f"${target_avg}"]
        trap_map = {
            f"${needed + 25}": "arithmetic_mistake",
            f"${needed - 25}": "arithmetic_mistake",
            f"${target_avg}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total 6-day target revenue = 6 * ${target_avg} = ${tot_target}.\n"
            f"Step 2: Sum of revenues from Monday to Friday = ${sum(sales)}.\n"
            f"Step 3: Saturday revenue needed = ${tot_target} - ${sum(sales)} = ${needed}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="missing_number_average",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5050: Adding Number to Average
# -----------------------------------------------------------------------------
def generate_adding_number_to_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_new_average_one_added",
        "find_added_value",
        "teacher_joins_class",
        "batsman_or_player_score",
        "multiple_items_added",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_new_average_one_added":
        n = random.randint(4, 9)
        orig_avg = random.randint(20, 50)
        # Added value chosen so that (n * orig_avg + val) % (n + 1) == 0
        delta = random.choice([2, 3, 4])
        val = orig_avg + delta * (n + 1)
        new_avg = orig_avg + delta
        question = (
            f"The average of {n} numbers is {orig_avg}. "
            f"If a new number equal to {val} is added to the set, what is the new average of all {n + 1} numbers?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg + 1), str(orig_avg), str((orig_avg + val) // 2)]
        trap_map = {
            str(new_avg + 1): "arithmetic_mistake",
            str(orig_avg): "conceptual_mistake",
            str((orig_avg + val) // 2): "average_weighted_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: New total sum with {val} added = {n * orig_avg} + {val} = {n * orig_avg + val}.\n"
            f"Step 3: New average = {n * orig_avg + val} / {n + 1} = {new_avg}."
        )

    elif subvariant == "find_added_value":
        n = random.randint(5, 12)
        orig_avg = random.randint(30, 70)
        delta = random.choice([1, 2, 3])
        new_avg = orig_avg + delta
        added_val = orig_avg + (n + 1) * delta
        question = (
            f"A group of {n} test scores had an average of {orig_avg}. "
            f"After adding one more test score, the average score increased to {new_avg}. "
            f"What was the value of the added test score?"
        )
        correct = str(added_val)
        wrong_unweighted = str(orig_avg + n * delta)
        distractors = [wrong_unweighted, str(new_avg + delta), str(added_val + 5)]
        trap_map = {
            wrong_unweighted: "setup_mistake",
            str(new_avg + delta): "average_weighted_mistake",
            str(added_val + 5): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: New total sum with {n + 1} scores = {n + 1} * {new_avg} = {(n + 1) * new_avg}.\n"
            f"Step 3: Added score = {(n + 1) * new_avg} - {n * orig_avg} = {added_val}."
        )

    elif subvariant == "teacher_joins_class":
        n_students = random.randint(14, 24)
        avg_age = random.choice([12, 13, 14, 15])
        delta = random.choice([1, 2])
        teacher_age = avg_age + (n_students + 1) * delta
        question = (
            f"In a classroom of {n_students} students, the average age is {avg_age} years. "
            f"When the teacher joins the class, the average age increases by {delta} year"
            + ("s" if delta > 1 else "")
            + ". How old is the teacher?"
        )
        correct = f"{teacher_age} years"
        wrong_setup = f"{avg_age + n_students * delta} years"
        distractors = [wrong_setup, f"{teacher_age - 3} years", f"{avg_age + delta} years"]
        trap_map = {
            wrong_setup: "setup_mistake",
            f"{teacher_age - 3} years": "arithmetic_mistake",
            f"{avg_age + delta} years": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total age of {n_students} students = {n_students} * {avg_age} = {n_students * avg_age}.\n"
            f"Step 2: Total members now = {n_students + 1}, with new average age = {avg_age + delta}.\n"
            f"Step 3: Total age of group = {n_students + 1} * {avg_age + delta} = {(n_students + 1) * (avg_age + delta)}.\n"
            f"Step 4: Teacher's age = {(n_students + 1) * (avg_age + delta)} - {n_students * avg_age} = {teacher_age} years."
        )

    elif subvariant == "batsman_or_player_score":
        innings = random.choice([8, 10, 12])
        avg = random.randint(35, 55)
        new_innings = innings + 1
        delta = random.choice([2, 3, 4])
        score = avg + new_innings * delta
        new_avg = avg + delta
        question = (
            f"A cricketer has an average of {avg} runs in {innings} innings. "
            f"In his next inning, he scores {score} runs. What is his new batting average?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg + 1), str((avg + score) // 2), str(avg + delta + 2)]
        trap_map = {
            str(new_avg + 1): "arithmetic_mistake",
            str((avg + score) // 2): "average_weighted_mistake",
            str(avg + delta + 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Runs scored in first {innings} innings = {innings} * {avg} = {innings * avg}.\n"
            f"Step 2: Total runs after {new_innings} innings = {innings * avg} + {score} = {innings * avg + score}.\n"
            f"Step 3: New average = {innings * avg + score} / {new_innings} = {new_avg} runs."
        )

    else:  # multiple_items_added
        n1 = 4
        a1 = random.randint(20, 30)
        n2 = 2
        a2 = random.randint(35, 45)
        combined_tot = n1 * a1 + n2 * a2
        combined_avg = combined_tot // (n1 + n2)
        # adjust a2 to make clean integer division
        rem = combined_tot % (n1 + n2)
        if rem != 0:
            a2 += (n1 + n2 - rem) // n2
            combined_tot = n1 * a1 + n2 * a2
            combined_avg = combined_tot // (n1 + n2)
        question = (
            f"A group of {n1} items has an average weight of {a1} kg. "
            f"Another {n2} items with an average weight of {a2} kg are added to the group. "
            f"What is the average weight of the combined {n1 + n2} items?"
        )
        correct = f"{combined_avg} kg"
        simple_mean = f"{(a1 + a2) // 2} kg"
        distractors = [simple_mean, f"{combined_avg + 2} kg", f"{combined_avg - 2} kg"]
        trap_map = {
            simple_mean: "average_weighted_mistake",
            f"{combined_avg + 2} kg": "arithmetic_mistake",
            f"{combined_avg - 2} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total weight of first group = {n1} * {a1} = {n1 * a1} kg.\n"
            f"Step 2: Total weight of second group = {n2} * {a2} = {n2 * a2} kg.\n"
            f"Step 3: Combined total weight = {n1 * a1} + {n2 * a2} = {combined_tot} kg.\n"
            f"Step 4: Combined average = {combined_tot} / ({n1} + {n2}) = {combined_avg} kg."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="adding_number_to_average",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5051: Removing Number from Average
# -----------------------------------------------------------------------------
def generate_removing_number_from_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_new_average_one_removed",
        "find_removed_value",
        "student_leaves_group",
        "replacement_in_average",
        "multiple_items_removed",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_new_average_one_removed":
        n = random.randint(6, 10)
        orig_avg = random.randint(30, 60)
        delta = random.choice([1, 2, 3])
        # remove a high number so avg drops by delta
        rem_val = orig_avg + (n - 1) * delta
        new_avg = orig_avg - delta
        question = (
            f"The average of {n} numbers is {orig_avg}. "
            f"If one number equal to {rem_val} is removed, what is the average of the remaining {n - 1} numbers?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg - 1), str(orig_avg), str(new_avg + 2)]
        trap_map = {
            str(new_avg - 1): "arithmetic_mistake",
            str(orig_avg): "conceptual_mistake",
            str(new_avg + 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: Remaining sum after removing {rem_val} = {n * orig_avg} - {rem_val} = {n * orig_avg - rem_val}.\n"
            f"Step 3: New average = ({n * orig_avg - rem_val}) / {n - 1} = {new_avg}."
        )

    elif subvariant == "find_removed_value":
        n = random.randint(5, 11)
        orig_avg = random.randint(25, 55)
        delta = random.choice([2, 3])
        new_avg = orig_avg - delta
        removed_val = orig_avg + (n - 1) * delta
        question = (
            f"The average of {n} observations is {orig_avg}. "
            f"When one observation is removed, the average of the remaining observations decreases to {new_avg}. "
            f"What was the value of the removed observation?"
        )
        correct = str(removed_val)
        wrong_setup = str(orig_avg + n * delta)
        distractors = [wrong_setup, str(removed_val - 4), str(new_avg - delta)]
        trap_map = {
            wrong_setup: "setup_mistake",
            str(removed_val - 4): "arithmetic_mistake",
            str(new_avg - delta): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total sum of {n} observations = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: Total sum of {n - 1} remaining observations = ({n - 1}) * {new_avg} = {(n - 1) * new_avg}.\n"
            f"Step 3: Removed observation = {n * orig_avg} - {(n - 1) * new_avg} = {removed_val}."
        )

    elif subvariant == "student_leaves_group":
        n = random.randint(8, 15)
        orig_wt = random.randint(50, 70)
        delta = 1
        leaving_wt = orig_wt + (n - 1) * delta
        question = (
            f"The average weight of {n} members of a sports team is {orig_wt} kg. "
            f"When one member leaves the team, the average weight of the remaining members drops by {delta} kg. "
            f"What was the weight of the member who left?"
        )
        correct = f"{leaving_wt} kg"
        wrong_sub = f"{orig_wt - (n - 1) * delta} kg"
        distractors = [wrong_sub, f"{leaving_wt + 2} kg", f"{orig_wt} kg"]
        trap_map = {
            wrong_sub: "sign_mistake",
            f"{leaving_wt + 2} kg": "arithmetic_mistake",
            f"{orig_wt} kg": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Original total weight = {n} * {orig_wt} = {n * orig_wt} kg.\n"
            f"Step 2: Remaining {n - 1} members have average weight {orig_wt - delta} kg.\n"
            f"Step 3: Remaining sum = {n - 1} * {orig_wt - delta} = {(n - 1) * (orig_wt - delta)} kg.\n"
            f"Step 4: Leaver's weight = {n * orig_wt} - {(n - 1) * (orig_wt - delta)} = {leaving_wt} kg."
        )

    elif subvariant == "replacement_in_average":
        n = random.randint(8, 20)
        old_val = random.randint(40, 80)
        delta = random.choice([2, 3, 4])
        new_val = old_val + n * delta
        question = (
            f"In a group of {n} individuals, a person weighing {old_val} kg is replaced by a new person. "
            f"As a result, the average weight of the group increases by {delta} kg. "
            f"What is the weight of the new person?"
        )
        correct = f"{new_val} kg"
        wrong_no_n = f"{old_val + delta} kg"
        distractors = [wrong_no_n, f"{old_val - n * delta} kg", f"{new_val + delta} kg"]
        trap_map = {
            wrong_no_n: "setup_mistake",
            f"{old_val - n * delta} kg": "sign_mistake",
            f"{new_val + delta} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Net increase in the total weight of the group = {n} members * {delta} kg = {n * delta} kg.\n"
            f"Step 2: Weight of new person = Weight of replaced person + Net Increase.\n"
            f"Step 3: New weight = {old_val} + {n * delta} = {new_val} kg."
        )

    else:  # multiple_items_removed
        n = 8
        orig_avg = 40
        rem_count = 2
        rem_avg = 55
        tot_orig = n * orig_avg  # 320
        tot_rem = rem_count * rem_avg  # 110
        rem_items = n - rem_count  # 6
        new_avg = (tot_orig - tot_rem) // rem_items  # 210 / 6 = 35
        question = (
            f"The average score of {n} students on an exam is {orig_avg}. "
            f"If {rem_count} students with an average score of {rem_avg} leave the class, "
            f"what is the average score of the remaining {rem_items} students?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg - 2), str((orig_avg + rem_avg) // 2), str(new_avg + 3)]
        trap_map = {
            str(new_avg - 2): "arithmetic_mistake",
            str((orig_avg + rem_avg) // 2): "average_weighted_mistake",
            str(new_avg + 3): "setup_mistake",
        }
        explanation = (
            f"Step 1: Original total score = {n} * {orig_avg} = {tot_orig}.\n"
            f"Step 2: Total score of leaving students = {rem_count} * {rem_avg} = {tot_rem}.\n"
            f"Step 3: Remaining total score = {tot_orig} - {tot_rem} = {tot_orig - tot_rem}.\n"
            f"Step 4: Remaining average = {tot_orig - tot_rem} / {rem_items} = {new_avg}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="removing_number_from_average",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5052: Average Change Shortcut
# -----------------------------------------------------------------------------
def generate_average_change_shortcut(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_added_via_deviation",
        "find_removed_via_deviation",
        "find_replacement_diff",
        "find_count_via_deviation",
        "sum_of_deviations_zero",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_added_via_deviation":
        # Deviation shortcut: Added = Old_Avg + (N+1)*Delta
        n = random.randint(10, 25)
        old_avg = random.randint(40, 80)
        delta = random.choice([2, 3])
        added_val = old_avg + (n + 1) * delta
        question = (
            f"A group of {n} employees has an average monthly bonus of ${old_avg}. "
            f"When a new employee joins, the average bonus of the group increases by ${delta}. "
            f"Using the deviation shortcut (New Value = Old Average + (N + 1) * Delta), "
            f"what is the bonus received by the new employee?"
        )
        correct = f"${added_val}"
        wrong_n = f"${old_avg + n * delta}"
        distractors = [wrong_n, f"${added_val + 5}", f"${old_avg + delta}"]
        trap_map = {
            wrong_n: "setup_mistake",
            f"${added_val + 5}": "arithmetic_mistake",
            f"${old_avg + delta}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: The new member must provide the previous average plus ${delta} for each member of the new group.\n"
            f"Step 2: Total members in new group = {n} + 1 = {n + 1}.\n"
            f"Step 3: Added bonus = Old Average + ({n + 1} * Delta) = ${old_avg} + ({n + 1} * ${delta}) = ${added_val}."
        )

    elif subvariant == "find_removed_via_deviation":
        # Deviation shortcut: Removed = Old_Avg + (N-1)*Delta (when average drops by delta)
        n = random.randint(12, 24)
        old_avg = random.randint(50, 80)
        delta = random.choice([1, 2])
        removed_val = old_avg + (n - 1) * delta
        question = (
            f"A cohort of {n} trainees had an average assessment score of {old_avg}. "
            f"When one trainee's score was removed, the average score of the remaining group dropped by {delta} point"
            + ("s" if delta > 1 else "")
            + ". What was the score of the removed trainee?"
        )
        correct = str(removed_val)
        wrong_sub = str(old_avg - (n - 1) * delta)
        distractors = [wrong_sub, str(old_avg + n * delta), str(removed_val + 2)]
        trap_map = {
            wrong_sub: "sign_mistake",
            str(old_avg + n * delta): "setup_mistake",
            str(removed_val + 2): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Because removing this score reduced the average for the remaining {n - 1} trainees by {delta},\n"
            f"the removed score contributed a total surplus of ({n - 1}) * {delta} above the mean.\n"
            f"Step 2: Removed score = {old_avg} + ({n - 1}) * {delta} = {removed_val}."
        )

    elif subvariant == "find_replacement_diff":
        n = random.randint(10, 30)
        delta = random.choice([1.5, 2.0, 2.5, 3.0])
        diff = int(round(n * delta))
        question = (
            f"In a team of {n} researchers, one person is replaced by a new recruit. "
            f"If the average age of the team decreases by {delta} years, "
            f"by how many years is the new recruit younger than the replaced researcher?"
        )
        correct = f"{diff} years"
        distractors = [f"{int(delta)} years", f"{diff + int(delta)} years", f"{int(round((n - 1) * delta))} years"]
        trap_map = {
            f"{int(delta)} years": "setup_mistake",
            f"{diff + int(delta)} years": "arithmetic_mistake",
            f"{int(round((n - 1) * delta))} years": "setup_mistake",
        }
        explanation = (
            f"Step 1: The total reduction across all {n} members is N * Delta.\n"
            f"Step 2: Age difference = {n} * {delta} = {diff} years."
        )

    elif subvariant == "find_count_via_deviation":
        # n = (X - B) / (B - A)
        old_avg = 50
        new_avg = 55
        added_val = 90
        # n = (90 - 55) / (55 - 50) = 35 / 5 = 7
        n = (added_val - new_avg) // (new_avg - old_avg)
        question = (
            f"A group of friends had an average test score of {old_avg}. "
            f"When an additional friend scoring {added_val} joined the group, "
            f"the average score rose to {new_avg}. "
            f"How many friends were originally in the group?"
        )
        correct = str(n)
        distractors = [str(n + 1), str(max(1, n - 1)), str((added_val - old_avg) // (new_avg - old_avg))]
        trap_map = {
            str(n + 1): "setup_mistake",
            str(max(1, n - 1)): "arithmetic_mistake",
            str((added_val - old_avg) // (new_avg - old_avg)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the deviation balance method: Initial Count n = (Added Value - New Average) / (New Average - Old Average).\n"
            f"Step 2: Surplus provided to existing members = {added_val} - {new_avg} = {added_val - new_avg}.\n"
            f"Step 3: Increase received per existing member = {new_avg} - {old_avg} = {new_avg - old_avg}.\n"
            f"Step 4: Initial Count = {added_val - new_avg} / {new_avg - old_avg} = {n} friends."
        )

    else:  # sum_of_deviations_zero
        # Deviations from mean always sum to 0
        devs = [-5, 8, -3, 2]
        last_dev = -sum(devs)
        devs_str = ", ".join([f"{'+' if d > 0 else ''}{d}" for d in devs])
        question = (
            f"For a set of 5 numbers, the deviations of the first 4 numbers from their arithmetic mean are "
            f"{devs_str}. What is the deviation of the fifth number from the mean?"
        )
        correct = f"{'+' if last_dev > 0 else ''}{last_dev}"
        wrong_sign = f"{'+' if -last_dev > 0 else ''}{-last_dev}"
        distractors = [wrong_sign, "0", "+1"]
        trap_map = {
            wrong_sign: "sign_mistake",
            "0": "conceptual_mistake",
            "+1": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: By mathematical definition, the sum of all deviations from the arithmetic mean is always zero: Sum(d_i) = 0.\n"
            f"Step 2: Sum of known deviations = {sum(devs)}.\n"
            f"Step 3: Deviation of the 5th number = -({sum(devs)}) = {correct}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="average_change_shortcut",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5053: Weighted Average
# -----------------------------------------------------------------------------
def generate_weighted_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_groups_find_combined",
        "find_ratio_of_counts",
        "three_groups_find_combined",
        "find_missing_group_average",
        "weighted_percentage_marks",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "two_groups_find_combined":
        # n1 * a1 + n2 * a2
        n1, a1, n2, a2 = random.choice([
            (20, 70, 30, 80),  # (1400 + 2400)/50 = 76
            (10, 60, 40, 75),  # (600 + 3000)/50 = 72
            (15, 80, 25, 60),  # (1200 + 1500)/40 = 67.5 -> let's make integer
            (12, 70, 18, 85),  # (840 + 1530)/30 = 2370/30 = 79
            (25, 64, 75, 80),  # (1600 + 6000)/100 = 76
        ])
        comb = (n1 * a1 + n2 * a2) // (n1 + n2)
        question = (
            f"Section A has {n1} students with an average score of {a1}. "
            f"Section B has {n2} students with an average score of {a2}. "
            f"What is the combined average score of all students in both sections?"
        )
        correct = str(comb)
        unweighted = str((a1 + a2) // 2)
        distractors = [unweighted, str(comb + 2), str(comb - 2)]
        trap_map = {
            unweighted: "average_weighted_mistake",
            str(comb + 2): "arithmetic_mistake",
            str(comb - 2): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Sum for Section A = {n1} * {a1} = {n1 * a1}.\n"
            f"Step 2: Sum for Section B = {n2} * {a2} = {n2 * a2}.\n"
            f"Step 3: Total sum = {n1 * a1} + {n2 * a2} = {n1 * a1 + n2 * a2}.\n"
            f"Step 4: Total students = {n1} + {n2} = {n1 + n2}.\n"
            f"Step 5: Combined Average = {n1 * a1 + n2 * a2} / {n1 + n2} = {comb}."
        )

    elif subvariant == "find_ratio_of_counts":
        # Alligation: n1/n2 = (a2 - a_avg) / (a_avg - a1)
        a1, a2 = 60, 90
        # choose a_avg = 72 => (90 - 72) : (72 - 60) = 18 : 12 = 3 : 2
        a_avg = 72
        d1 = a2 - a_avg  # 18
        d2 = a_avg - a1  # 12
        g = gcd(d1, d2)
        r1, r2 = d1 // g, d2 // g
        question = (
            f"In a company, junior developers have an average hourly rate of ${a1} and senior developers have an average hourly rate of ${a2}. "
            f"If the company-wide average hourly rate for developers is ${a_avg}, what is the ratio of junior developers to senior developers?"
        )
        correct = f"{r1}:{r2}"
        distractors = [f"{r2}:{r1}", "1:1", f"{a1 // 10}:{a2 // 10}"]
        trap_map = {
            f"{r2}:{r1}": "ratio_interpretation_mistake",
            "1:1": "average_weighted_mistake",
            f"{a1 // 10}:{a2 // 10}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Apply the alligation / weighted average ratio rule:\n"
            f"   (Junior Count) / (Senior Count) = |Senior Avg - Overall Avg| / |Overall Avg - Junior Avg|.\n"
            f"Step 2: Distance from Senior Avg = {a2} - {a_avg} = {d1}.\n"
            f"Step 3: Distance from Junior Avg = {a_avg} - {a1} = {d2}.\n"
            f"Step 4: Ratio = {d1}:{d2} = {r1}:{r2} in simplest terms."
        )

    elif subvariant == "three_groups_find_combined":
        n1, a1 = 10, 60
        n2, a2 = 20, 75
        n3, a3 = 30, 90
        tot_pts = n1 * a1 + n2 * a2 + n3 * a3  # 600 + 1500 + 2700 = 4800
        tot_n = n1 + n2 + n3  # 60
        comb = tot_pts // tot_n  # 80
        question = (
            f"Three training batches of sizes {n1}, {n2}, and {n3} scored averages of {a1}, {a2}, and {a3} respectively. "
            f"What is the overall average score across all three batches?"
        )
        correct = str(comb)
        unweighted = str((a1 + a2 + a3) // 3)
        distractors = [unweighted, str(comb + 3), str(comb - 3)]
        trap_map = {
            unweighted: "average_weighted_mistake",
            str(comb + 3): "arithmetic_mistake",
            str(comb - 3): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total points = ({n1} * {a1}) + ({n2} * {a2}) + ({n3} * {a3}) = {n1 * a1} + {n2 * a2} + {n3 * a3} = {tot_pts}.\n"
            f"Step 2: Total participants = {n1} + {n2} + {n3} = {tot_n}.\n"
            f"Step 3: Combined Average = {tot_pts} / {tot_n} = {comb}."
        )

    elif subvariant == "find_missing_group_average":
        tot_n = 50
        n1 = 20
        n2 = 30
        comb_avg = 74
        a1 = 65
        # 50 * 74 - 20 * 65 = 3700 - 1300 = 2400. 2400 / 30 = 80
        a2 = (tot_n * comb_avg - n1 * a1) // n2
        question = (
            f"A cohort of {tot_n} students has an overall average score of {comb_avg}. "
            f"If {n1} of the students scored an average of {a1}, "
            f"what was the average score of the remaining {n2} students?"
        )
        correct = str(a2)
        distractors = [str(comb_avg), str(a2 + 4), str(a2 - 4)]
        trap_map = {
            str(comb_avg): "conceptual_mistake",
            str(a2 + 4): "arithmetic_mistake",
            str(a2 - 4): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total score for all {tot_n} students = {tot_n} * {comb_avg} = {tot_n * comb_avg}.\n"
            f"Step 2: Total score for first {n1} students = {n1} * {a1} = {n1 * a1}.\n"
            f"Step 3: Total score for remaining {n2} students = {tot_n * comb_avg} - {n1 * a1} = {tot_n * comb_avg - n1 * a1}.\n"
            f"Step 4: Average for remaining students = {tot_n * comb_avg - n1 * a1} / {n2} = {a2}."
        )

    else:  # weighted_percentage_marks
        w1, w2, w3 = 20, 30, 50
        s1, s2, s3 = 90, 80, 70
        tot = (w1 * s1 + w2 * s2 + w3 * s3) // 100  # 1800 + 2400 + 3500 = 7700 // 100 = 77
        question = (
            f"A course grade is calculated with weights: Homework {w1}%, Midterm Exam {w2}%, and Final Exam {w3}%. "
            f"If a student scores {s1}% on Homework, {s2}% on the Midterm, and {s3}% on the Final Exam, "
            f"what is the student's overall weighted course grade?"
        )
        correct = f"{tot}%"
        simple = f"{(s1 + s2 + s3) // 3}%"
        distractors = [simple, f"{tot + 3}%", f"{tot - 3}%"]
        trap_map = {
            simple: "average_weighted_mistake",
            f"{tot + 3}%": "arithmetic_mistake",
            f"{tot - 3}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Compute weighted components:\n"
            f"   Homework: {w1}% * {s1} = {w1 * s1 / 100:.1f}\n"
            f"   Midterm: {w2}% * {s2} = {w2 * s2 / 100:.1f}\n"
            f"   Final Exam: {w3}% * {s3} = {w3 * s3 / 100:.1f}\n"
            f"Step 2: Add weighted scores: {tot}%."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="weighted_average",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5054: Weighted Average Intuition
# -----------------------------------------------------------------------------
def generate_weighted_average_intuition(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "pulled_towards_larger_group",
        "equal_sizes_vs_unequal",
        "teeter_totter_leverage",
        "quick_elimination_bounds",
        "weighted_average_ds_style",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "pulled_towards_larger_group":
        # Group A: 80 people, avg 70. Group B: 20 people, avg 90. Midpoint 80.
        # Combined avg = (5600 + 1800)/100 = 74.
        question = (
            "Class A has 80 students with an average exam score of 70. "
            "Class B has 20 students with an average exam score of 90. "
            "Without calculating the exact number, the combined average score of both classes must be:"
        )
        correct = "Between 70 and 80 (closer to 70)"
        distractors = [
            "Exactly 80 (the simple arithmetic midpoint)",
            "Between 80 and 90 (closer to 90)",
            "Greater than 90",
        ]
        trap_map = {
            "Exactly 80 (the simple arithmetic midpoint)": "average_weighted_mistake",
            "Between 80 and 90 (closer to 90)": "conceptual_mistake",
            "Greater than 90": "conceptual_mistake",
        }
        explanation = (
            "Step 1: The midpoint of 70 and 90 is (70 + 90) / 2 = 80.\n"
            "Step 2: A weighted average is always pulled toward the group with larger weight.\n"
            "Step 3: Since Class A has 80 students and Class B has only 20, the combined average must be strictly closer to 70 than to 90, meaning it lies between 70 and 80."
        )

    elif subvariant == "equal_sizes_vs_unequal":
        question = (
            "Group X has an average score of 60 and Group Y has an average score of 80. "
            "If both groups initially have 30 members, their combined average is 70. "
            "If 30 additional members are added to Group Y while Group X remains at 30 members, "
            "what will happen to the combined average?"
        )
        correct = "It increases to 73.33 (pulled toward 80)"
        distractors = [
            "It remains unchanged at 70",
            "It decreases toward 60",
            "It increases to 80 exactly",
        ]
        trap_map = {
            "It remains unchanged at 70": "conceptual_mistake",
            "It decreases toward 60": "conceptual_mistake",
            "It increases to 80 exactly": "conceptual_mistake",
        }
        explanation = (
            "Step 1: New sizes: Group X has 30, Group Y has 60 (ratio 1:2).\n"
            "Step 2: Combined average = (1 * 60 + 2 * 80) / 3 = 220 / 3 = 73.33.\n"
            "Step 3: Increasing the relative weight of the higher group pulls the combined average toward 80."
        )

    elif subvariant == "teeter_totter_leverage":
        # Dept A avg 50k, Dept B avg 80k. Combined avg 55k.
        # Dist to A = 5k, Dist to B = 25k. Ratio A:B = 25:5 = 5:1.
        question = (
            "The average annual salary in Division A is $50,000, and in Division B it is $80,000. "
            "If the overall average salary across both divisions combined is $55,000, "
            "what is the ratio of the number of employees in Division A to Division B?"
        )
        correct = "5:1"
        distractors = ["1:5", "1:1", "3:1"]
        trap_map = {
            "1:5": "ratio_interpretation_mistake",
            "1:1": "average_weighted_mistake",
            "3:1": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Teeter-totter principle: Distance to Division A = $55,000 - $50,000 = $5,000.\n"
            "Step 2: Distance to Division B = $80,000 - $55,000 = $25,000.\n"
            "Step 3: The ratio of headcount is inversely proportional to distances:\n"
            "   (Headcount A) / (Headcount B) = 25,000 / 5,000 = 5 / 1 = 5:1."
        )

    elif subvariant == "quick_elimination_bounds":
        # Group 1 avg 62, Group 2 avg 88. Possible combined avg.
        question = (
            "Group 1 has an average score of 62 and Group 2 has an average score of 88. "
            "Regardless of group sizes, which of the following is a possible value for their combined average?"
        )
        correct = "78"
        distractors = ["58", "62", "91"]
        trap_map = {
            "58": "conceptual_mistake",
            "62": "conceptual_mistake",
            "91": "conceptual_mistake",
        }
        explanation = (
            "Step 1: Any weighted average of two distinct groups must lie strictly between their two averages: 62 < Combined Avg < 88.\n"
            "Step 2: 58 is below the minimum (62), 62 would require Group 2 to have 0 members, and 91 is above the maximum (88).\n"
            "Step 3: Only 78 lies strictly within the range (62, 88)."
        )

    else:  # weighted_average_ds_style
        # Men avg 6.0, Women avg 8.5. Combined avg 7.5.
        # Dist to Men = 1.5, Dist to Women = 1.0.
        # Men : Women = 1.0 : 1.5 = 2 : 3. Women fraction = 3/5 = 60%.
        question = (
            "In a satisfaction survey, male customers gave an average score of 6.0 and female customers gave an average score of 8.5. "
            "If the overall average satisfaction score was 7.5, what percentage of the surveyed customers were women?"
        )
        correct = "60%"
        distractors = ["40%", "50%", "75%"]
        trap_map = {
            "40%": "careless_mistake",
            "50%": "average_weighted_mistake",
            "75%": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Distance from male average = |7.5 - 6.0| = 1.5.\n"
            "Step 2: Distance from female average = |8.5 - 7.5| = 1.0.\n"
            "Step 3: Ratio of Men to Women = 1.0 : 1.5 = 2 : 3.\n"
            "Step 4: Percentage of women = 3 / (2 + 3) * 100% = 3/5 * 100% = 60%."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="weighted_average_intuition",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Pattern 5055: GMAT Mixed Questions
# -----------------------------------------------------------------------------
def generate_gmat_mixed_questions(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "ratio_and_percentage",
        "ratio_and_average",
        "percentage_and_profit_loss",
        "fraction_and_percentage_shift",
        "ratio_average_percentage_trio",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "ratio_and_percentage":
        # Men : Women = 3 : 2. 20% men certified, 30% women certified.
        # Total certified = (3*20 + 2*30)/5 = (60 + 60)/5 = 24%.
        m, w = 3, 2
        pm, pw = 20, 30
        pct = (m * pm + w * pw) // (m + w)
        question = (
            f"In an engineering firm, the ratio of male to female employees is {m}:{w}. "
            f"If {pm}% of the male employees and {pw}% of the female employees hold professional certifications, "
            f"what percentage of all employees in the firm hold professional certifications?"
        )
        correct = f"{pct}%"
        simple_avg = f"{(pm + pw) // 2}%"
        distractors = [simple_avg, f"{pct + 2}%", f"{pct - 2}%"]
        trap_map = {
            simple_avg: "average_weighted_mistake",
            f"{pct + 2}%": "arithmetic_mistake",
            f"{pct - 2}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Assume a convenient total population based on the ratio {m}:{w}, say {m * 10} males and {w * 10} females (total = {(m + w) * 10}).\n"
            f"Step 2: Certified males = {pm}% of {m * 10} = {m * pm // 10}.\n"
            f"Step 3: Certified females = {pw}% of {w * 10} = {w * pw // 10}.\n"
            f"Step 4: Total certified = {m * pm // 10 + w * pw // 10} out of {(m + w) * 10}.\n"
            f"Step 5: Overall percentage = {pct}%."
        )

    elif subvariant == "ratio_and_average":
        # Box A and B item counts in ratio 2:3. Avg weight in A is 40 kg, in B is 60 kg.
        # Combined avg = (2*40 + 3*60)/5 = (80 + 180)/5 = 260/5 = 52 kg.
        r_a, r_b = 2, 3
        w_a, w_b = 40, 60
        comb_wt = (r_a * w_a + r_b * w_b) // (r_a + r_b)
        question = (
            f"The number of parcels in Warehouse A and Warehouse B is in the ratio {r_a}:{r_b}. "
            f"If the average weight of parcels in Warehouse A is {w_a} kg and in Warehouse B is {w_b} kg, "
            f"what is the average weight of a parcel across both warehouses combined?"
        )
        correct = f"{comb_wt} kg"
        simple_avg = f"{(w_a + w_b) // 2} kg"
        distractors = [simple_avg, f"{comb_wt + 3} kg", f"{comb_wt - 3} kg"]
        trap_map = {
            simple_avg: "average_weighted_mistake",
            f"{comb_wt + 3} kg": "arithmetic_mistake",
            f"{comb_wt - 3} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Weighted average formula = ({r_a} * {w_a} + {r_b} * {w_b}) / ({r_a} + {r_b}).\n"
            f"Step 2: Sum of weighted weights = {r_a * w_a} + {r_b * w_b} = {r_a * w_a + r_b * w_b}.\n"
            f"Step 3: Total ratio parts = {r_a + r_b}.\n"
            f"Step 4: Overall average weight = {r_a * w_a + r_b * w_b} / {r_a + r_b} = {comb_wt} kg."
        )

    elif subvariant == "percentage_and_profit_loss":
        # Markup 40%, Discount 20% -> net profit = 40 - 20 - (40*20)/100 = 12%.
        m_pct = 40
        d_pct = 20
        net_profit = m_pct - d_pct - (m_pct * d_pct) // 100
        question = (
            f"A retailer marks an item {m_pct}% above its original cost price, "
            f"and then offers a discount of {d_pct}% off the marked price. "
            f"What is the retailer's net profit percentage on the cost price?"
        )
        correct = f"{net_profit}%"
        wrong_sub = f"{m_pct - d_pct}%"
        distractors = [wrong_sub, f"{net_profit - 4}%", f"{net_profit + 4}%"]
        trap_map = {
            wrong_sub: "percentage_base_mistake",
            f"{net_profit - 4}%": "arithmetic_mistake",
            f"{net_profit + 4}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Let the cost price CP = $100.\n"
            f"Step 2: Marked price MP = $100 * 1.{m_pct} = ${100 + m_pct}.\n"
            f"Step 3: Selling price SP after {d_pct}% discount = ${100 + m_pct} * (1 - {d_pct}/100) = ${100 + m_pct} * 0.8 = ${100 + net_profit}.\n"
            f"Step 4: Net profit = SP - CP = ${100 + net_profit} - $100 = {net_profit}%."
        )

    elif subvariant == "fraction_and_percentage_shift":
        # Increase by 25% (+1/4), then decrease by 20% (-1/5) => net 0% change.
        question = (
            "A company's quarterly stock price increases by 25% in the first quarter, "
            "and then decreases by 20% in the second quarter. "
            "What is the net percentage change in the stock price over the two quarters?"
        )
        correct = "0% (no change)"
        distractors = ["+5% increase", "-5% decrease", "+2.5% increase"]
        trap_map = {
            "+5% increase": "percentage_base_mistake",
            "-5% decrease": "conceptual_mistake",
            "+2.5% increase": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Let the initial stock price be 100.\n"
            "Step 2: After a 25% increase, the price becomes 100 * 1.25 = 125.\n"
            "Step 3: A 20% decrease on 125 is 125 * 0.20 = 25.\n"
            "Step 4: Final price = 125 - 25 = 100.\n"
            "Step 5: The net percentage change is 0% (the price returns exactly to its starting value)."
        )

    else:  # ratio_average_percentage_trio
        # Ratio 2:2:1, salaries 80k, 60k, 50k -> (160 + 120 + 50)/5 = 330/5 = $66,000.
        r1, r2, r3 = 2, 2, 1
        s1, s2, s3 = 80, 60, 50
        avg_sal = (r1 * s1 + r2 * s2 + r3 * s3) * 1000 // (r1 + r2 + r3)
        question = (
            f"A startup employs engineers, marketers, and administrators in the ratio {r1}:{r2}:{r3}. "
            f"The average annual salaries are ${s1},000 for engineers, ${s2},000 for marketers, and ${s3},000 for administrators. "
            f"What is the company-wide average annual salary per employee?"
        )
        correct = f"${avg_sal:,}"
        unweighted = f"${(s1 + s2 + s3) * 1000 // 3:,}"
        distractors = [unweighted, f"${avg_sal + 4000:,}", f"${avg_sal - 4000:,}"]
        trap_map = {
            unweighted: "average_weighted_mistake",
            f"${avg_sal + 4000:,}": "arithmetic_mistake",
            f"${avg_sal - 4000:,}": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total headcount weight = {r1} + {r2} + {r3} = {r1 + r2 + r3}.\n"
            f"Step 2: Total weighted payroll = ({r1} * ${s1},000) + ({r2} * ${s2},000) + ({r3} * ${s3},000) = ${r1*s1 + r2*s2 + r3*s3},000.\n"
            f"Step 3: Average salary = ${r1*s1 + r2*s2 + r3*s3},000 / {r1 + r2 + r3} = ${avg_sal:,}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="gmat_mixed_questions",
        subvariant=subvariant,
    )


# -----------------------------------------------------------------------------
# Metadata and Generator Registry
# -----------------------------------------------------------------------------

DAY4_PATTERNS_METADATA: Dict[Any, Dict[str, Any]] = {
    5040: {
        "id": 5040,
        "name": "ratio_basics",
        "description": "Interpret, simplify, equivalent ratios, compare, convert to actual quantities.",
        "variants": [
            "interpret_ratio",
            "simplify_ratio",
            "equivalent_ratios",
            "compare_ratios",
            "convert_to_actual",
        ],
        "variant_names": [
            "interpret_ratio",
            "simplify_ratio",
            "equivalent_ratios",
            "compare_ratios",
            "convert_to_actual",
        ],
    },
    5041: {
        "id": 5041,
        "name": "ratio_with_total",
        "description": "Divide a total amount among parts using given ratios.",
        "variants": [
            "two_parts_find_one",
            "two_parts_difference",
            "three_parts_find_one",
            "three_parts_extremes_diff",
            "ratio_with_total_word_problem",
        ],
        "variant_names": [
            "two_parts_find_one",
            "two_parts_difference",
            "three_parts_find_one",
            "three_parts_extremes_diff",
            "ratio_with_total_word_problem",
        ],
    },
    5042: {
        "id": 5042,
        "name": "ratio_one_value_known",
        "description": "Calculate missing parts, totals, or differences when one ratio value is known.",
        "variants": [
            "first_known_find_second",
            "second_known_find_first",
            "one_known_find_total",
            "one_known_find_difference",
            "three_way_one_known",
        ],
        "variant_names": [
            "first_known_find_second",
            "second_known_find_first",
            "one_known_find_total",
            "one_known_find_difference",
            "three_way_one_known",
        ],
    },
    5043: {
        "id": 5043,
        "name": "ratio_changes",
        "description": "Analyze ratio shifts when quantities are added, removed, or transferred.",
        "variants": [
            "add_to_one_part",
            "remove_from_one_part",
            "ratio_becomes_equal",
            "add_to_both_parts",
            "remove_from_both_parts",
        ],
        "variant_names": [
            "add_to_one_part",
            "remove_from_one_part",
            "ratio_becomes_equal",
            "add_to_both_parts",
            "remove_from_both_parts",
        ],
    },
    5044: {
        "id": 5044,
        "name": "ratio_variables_x_method",
        "description": "Algebraic x-multiplier method for ratios with sums, differences, products, and squares.",
        "variants": [
            "linear_relation_x",
            "difference_given_x",
            "sum_of_squares_x",
            "product_given_x",
            "consecutive_ratio_equations",
        ],
        "variant_names": [
            "linear_relation_x",
            "difference_given_x",
            "sum_of_squares_x",
            "product_given_x",
            "consecutive_ratio_equations",
        ],
    },
    5045: {
        "id": 5045,
        "name": "proportion",
        "description": "Direct scale factor, cross-multiplication, fourth, third, and mean proportionals.",
        "variants": [
            "fourth_proportional",
            "mean_proportional",
            "third_proportional",
            "cross_multiplication_algebra",
            "scale_factor_proportion",
        ],
        "variant_names": [
            "fourth_proportional",
            "mean_proportional",
            "third_proportional",
            "cross_multiplication_algebra",
            "scale_factor_proportion",
        ],
    },
    5046: {
        "id": 5046,
        "name": "direct_proportion",
        "description": "Direct variation relationships: cost, fuel consumption, and production output.",
        "variants": [
            "items_and_cost",
            "distance_and_fuel",
            "hours_and_production",
            "weight_and_price",
            "speed_constant_time",
        ],
        "variant_names": [
            "items_and_cost",
            "distance_and_fuel",
            "hours_and_production",
            "weight_and_price",
            "speed_constant_time",
        ],
    },
    5047: {
        "id": 5047,
        "name": "inverse_proportion",
        "description": "Inverse variation relationships: workers & days, speed & time, and equipment.",
        "variants": [
            "workers_and_days",
            "speed_and_time",
            "pipes_or_machines",
            "provisions_and_people",
            "gear_teeth_revolutions",
        ],
        "variant_names": [
            "workers_and_days",
            "speed_and_time",
            "pipes_or_machines",
            "provisions_and_people",
            "gear_teeth_revolutions",
        ],
    },
    5048: {
        "id": 5048,
        "name": "average_basics",
        "description": "Fundamental arithmetic mean calculations, total sum derivation, and consecutive sequence averages.",
        "variants": [
            "compute_average",
            "find_sum_from_average",
            "find_count_from_sum_and_avg",
            "average_of_consecutive_integers",
            "average_of_multiples",
        ],
        "variant_names": [
            "compute_average",
            "find_sum_from_average",
            "find_count_from_sum_and_avg",
            "average_of_consecutive_integers",
            "average_of_multiples",
        ],
    },
    5049: {
        "id": 5049,
        "name": "missing_number_average",
        "description": "Determine missing elements given group averages, targets, or inter-element relationships.",
        "variants": [
            "one_missing_in_set",
            "test_score_target",
            "consecutive_series_with_unknown",
            "two_missing_with_relation",
            "missing_sales_or_daily_target",
        ],
        "variant_names": [
            "one_missing_in_set",
            "test_score_target",
            "consecutive_series_with_unknown",
            "two_missing_with_relation",
            "missing_sales_or_daily_target",
        ],
    },
    5050: {
        "id": 5050,
        "name": "adding_number_to_average",
        "description": "Compute updated group averages or identify added values when new items or members join.",
        "variants": [
            "find_new_average_one_added",
            "find_added_value",
            "teacher_joins_class",
            "batsman_or_player_score",
            "multiple_items_added",
        ],
        "variant_names": [
            "find_new_average_one_added",
            "find_added_value",
            "teacher_joins_class",
            "batsman_or_player_score",
            "multiple_items_added",
        ],
    },
    5051: {
        "id": 5051,
        "name": "removing_number_from_average",
        "description": "Analyze shifts in average when elements are removed or replaced in a dataset.",
        "variants": [
            "find_new_average_one_removed",
            "find_removed_value",
            "student_leaves_group",
            "replacement_in_average",
            "multiple_items_removed",
        ],
        "variant_names": [
            "find_new_average_one_removed",
            "find_removed_value",
            "student_leaves_group",
            "replacement_in_average",
            "multiple_items_removed",
        ],
    },
    5052: {
        "id": 5052,
        "name": "average_change_shortcut",
        "description": "Apply net deviation shortcuts to rapidly solve average change and replacement questions.",
        "variants": [
            "find_added_via_deviation",
            "find_removed_via_deviation",
            "find_replacement_diff",
            "find_count_via_deviation",
            "sum_of_deviations_zero",
        ],
        "variant_names": [
            "find_added_via_deviation",
            "find_removed_via_deviation",
            "find_replacement_diff",
            "find_count_via_deviation",
            "sum_of_deviations_zero",
        ],
    },
    5053: {
        "id": 5053,
        "name": "weighted_average",
        "description": "Combine averages across multiple groups with unequal weights or determine group weights.",
        "variants": [
            "two_groups_find_combined",
            "find_ratio_of_counts",
            "three_groups_find_combined",
            "find_missing_group_average",
            "weighted_percentage_marks",
        ],
        "variant_names": [
            "two_groups_find_combined",
            "find_ratio_of_counts",
            "three_groups_find_combined",
            "find_missing_group_average",
            "weighted_percentage_marks",
        ],
    },
    5054: {
        "id": 5054,
        "name": "weighted_average_intuition",
        "description": "Leverage visual and teeter-totter intuition to quickly eliminate choices in weighted average problems.",
        "variants": [
            "pulled_towards_larger_group",
            "equal_sizes_vs_unequal",
            "teeter_totter_leverage",
            "quick_elimination_bounds",
            "weighted_average_ds_style",
        ],
        "variant_names": [
            "pulled_towards_larger_group",
            "equal_sizes_vs_unequal",
            "teeter_totter_leverage",
            "quick_elimination_bounds",
            "weighted_average_ds_style",
        ],
    },
    5055: {
        "id": 5055,
        "name": "gmat_mixed_questions",
        "description": "Multi-topic integration combining ratios, averages, percentages, and profit/loss.",
        "variants": [
            "ratio_and_percentage",
            "ratio_and_average",
            "percentage_and_profit_loss",
            "fraction_and_percentage_shift",
            "ratio_average_percentage_trio",
        ],
        "variant_names": [
            "ratio_and_percentage",
            "ratio_and_average",
            "percentage_and_profit_loss",
            "fraction_and_percentage_shift",
            "ratio_average_percentage_trio",
        ],
    },
}

# Add string and ID aliases to DAY4_PATTERNS_METADATA for flexibility
for _pid in list(DAY4_PATTERNS_METADATA.keys()):
    _data = DAY4_PATTERNS_METADATA[_pid]
    DAY4_PATTERNS_METADATA[str(_pid)] = _data
    DAY4_PATTERNS_METADATA[_data["name"]] = _data


DAY4_GENERATORS: Dict[Any, Any] = {
    # Keyed by pattern name
    "ratio_basics": generate_ratio_basics,
    "ratio_with_total": generate_ratio_with_total,
    "ratio_one_value_known": generate_ratio_one_value_known,
    "ratio_changes": generate_ratio_changes,
    "ratio_variables_x_method": generate_ratio_variables_x_method,
    "proportion": generate_proportion,
    "direct_proportion": generate_direct_proportion,
    "inverse_proportion": generate_inverse_proportion,
    "average_basics": generate_average_basics,
    "missing_number_average": generate_missing_number_average,
    "adding_number_to_average": generate_adding_number_to_average,
    "removing_number_from_average": generate_removing_number_from_average,
    "average_change_shortcut": generate_average_change_shortcut,
    "weighted_average": generate_weighted_average,
    "weighted_average_intuition": generate_weighted_average_intuition,
    "gmat_mixed_questions": generate_gmat_mixed_questions,
    # Keyed by integer pattern ID
    5040: generate_ratio_basics,
    5041: generate_ratio_with_total,
    5042: generate_ratio_one_value_known,
    5043: generate_ratio_changes,
    5044: generate_ratio_variables_x_method,
    5045: generate_proportion,
    5046: generate_direct_proportion,
    5047: generate_inverse_proportion,
    5048: generate_average_basics,
    5049: generate_missing_number_average,
    5050: generate_adding_number_to_average,
    5051: generate_removing_number_from_average,
    5052: generate_average_change_shortcut,
    5053: generate_weighted_average,
    5054: generate_weighted_average_intuition,
    5055: generate_gmat_mixed_questions,
    # Keyed by string pattern ID
    "5040": generate_ratio_basics,
    "5041": generate_ratio_with_total,
    "5042": generate_ratio_one_value_known,
    "5043": generate_ratio_changes,
    "5044": generate_ratio_variables_x_method,
    "5045": generate_proportion,
    "5046": generate_direct_proportion,
    "5047": generate_inverse_proportion,
    "5048": generate_average_basics,
    "5049": generate_missing_number_average,
    "5050": generate_adding_number_to_average,
    "5051": generate_removing_number_from_average,
    "5052": generate_average_change_shortcut,
    "5053": generate_weighted_average,
    "5054": generate_weighted_average_intuition,
    "5055": generate_gmat_mixed_questions,
}
