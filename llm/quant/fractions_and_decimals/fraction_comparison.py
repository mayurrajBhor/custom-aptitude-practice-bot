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

def generate_fraction_comparison(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["same_denominator", "same_numerator", "cross_multiplication", "ordering"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "same_denominator":
        d = random.randint(7, 19)
        a = random.randint(2, d - 2)
        b = random.randint(1, a - 1)
        correct = f"{a}/{d} > {b}/{d}"
        candidates = [
            (f"{a}/{d} < {b}/{d}", "conceptual_mistake"),
            (f"{b}/{d} > {a}/{d}", "careless_mistake"),
            (f"{a}/{d} = {b}/{d}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Which comparison statement correctly relates {a}/{d} and {b}/{d}?"
        expl = (
            f"When two positive fractions share the same denominator, the fraction with the larger "
            f"numerator is larger.\n"
            f"Since {a} > {b}, {a}/{d} > {b}/{d}."
        )

    elif variant == "same_numerator":
        n = random.randint(3, 9)
        a = random.randint(4, 11)
        b = random.randint(a + 1, 16)
        # Note: n/a > n/b because a < b
        correct = f"{n}/{a}"
        candidates = [
            (f"{n}/{b}", "conceptual_mistake"),
            ("They are equal", "formula_selection_mistake"),
            ("Cannot be determined", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Which of the following two fractions is greater: {n}/{a} or {n}/{b}?"
        expl = (
            f"When two positive fractions share the same numerator, dividing by a smaller denominator "
            f"yields larger individual pieces.\n"
            f"Since {a} < {b}, {n}/{a} > {n}/{b}.\n"
            f"Therefore, the greater fraction is {correct}. "
            f"(Trap: Do not assume a larger denominator makes a fraction bigger!)"
        )

    elif variant == "cross_multiplication":
        a = random.randint(3, 8)
        b = random.randint(a + 1, 11)
        c = random.randint(3, 8)
        d = random.randint(c + 1, 11)
        while a * d == b * c or a == c or b == d:
            c = random.randint(3, 9)
            d = random.randint(c + 1, 12)

        prod1 = a * d
        prod2 = b * c
        if prod1 > prod2:
            correct = f"{a}/{b} > {c}/{d}"
            wrong_rel = f"{a}/{b} < {c}/{d}"
        else:
            correct = f"{a}/{b} < {c}/{d}"
            wrong_rel = f"{a}/{b} > {c}/{d}"

        candidates = [
            (wrong_rel, "formula_selection_mistake"),
            (f"{a}/{b} = {c}/{d}", "arithmetic_mistake"),
            (f"{c}/{d} > {a}/{b}" if prod1 > prod2 else f"{c}/{d} < {a}/{b}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Using cross-multiplication, compare {a}/{b} and {c}/{d}."
        expl = (
            f"To compare a/b and c/d, compute the cross-products:\n"
            f"Left cross-product: {a} × {d} = {prod1}\n"
            f"Right cross-product: {b} × {c} = {prod2}\n"
            f"Since {prod1} {' > ' if prod1 > prod2 else ' < '}{prod2}, it follows that {correct}."
        )

    else:  # ordering
        # 3 distinct fractions to order in ascending order
        f_list = [
            (1, 3, "1/3"),
            (2, 5, "2/5"),
            (1, 2, "1/2"),
            (3, 5, "3/5"),
            (2, 3, "2/3"),
            (3, 4, "3/4"),
            (5, 6, "5/6"),
        ]
        selected = random.sample(f_list, 3)
        selected.sort(key=lambda item: item[0] / item[1])

        s0, s1, s2 = selected[0][2], selected[1][2], selected[2][2]
        correct = f"{s0} < {s1} < {s2}"

        candidates = [
            (f"{s2} < {s1} < {s0}", "careless_mistake"),
            (f"{s1} < {s0} < {s2}", "arithmetic_mistake"),
            (f"{s0} < {s2} < {s1}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Which of the following arranges the fractions {s1}, {s0}, and {s2} in ascending order (least to greatest)?"
        expl = (
            f"Convert each fraction to a decimal or find a common denominator:\n"
            f"- {selected[0][2]} = {round(selected[0][0]/selected[0][1], 3)}\n"
            f"- {selected[1][2]} = {round(selected[1][0]/selected[1][1], 3)}\n"
            f"- {selected[2][2]} = {round(selected[2][0]/selected[2][1], 3)}\n"
            f"Arranging from least to greatest gives {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_comparison",
        subvariant=variant,
    )

