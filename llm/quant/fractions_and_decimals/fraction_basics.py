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

def generate_fraction_basics(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["identify_terms", "division_interpretation", "classify_fraction", "shaded_parts_concept"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "identify_terms":
        if level <= 2:
            num = random.randint(3, 9)
            den = random.randint(num + 1, 15)
            ask_num = random.choice([True, False])
        elif level <= 4:
            num = random.randint(11, 29)
            den = random.randint(31, 59)
            ask_num = random.choice([True, False])
        else:
            # Level 5: Reduced term identification or evaluation
            g = random.randint(3, 7)
            base_n = random.randint(2, 5)
            base_d = random.randint(base_n + 1, 9)
            while math.gcd(base_n, base_d) > 1:
                base_d = random.randint(base_n + 1, 11)
            num = g * base_n
            den = g * base_d
            ask_num = False  # Ask simplified denominator
            q_text = (
                f"In the fraction {num}/{den}, what is the denominator after the fraction "
                f"is reduced to its lowest terms?"
            )
            correct = str(base_d)
            candidates = [
                (str(den), "conceptual_mistake"),
                (str(base_n), "careless_mistake"),
                (str(base_d + 1), "arithmetic_mistake"),
                (str(base_d * 2), "formula_selection_mistake"),
            ]
            distractors, trap_map = _clean_distractors(correct, candidates)
            expl = (
                f"Step 1: Find the GCD of {num} and {den}, which is {g}.\n"
                f"Step 2: Divide numerator and denominator by {g}: {num} ÷ {g} = {base_n}, and {den} ÷ {g} = {base_d}.\n"
                f"The reduced fraction is {base_n}/{base_d}, so the simplified denominator is {base_d}."
            )
            return make_mcq(
                question=q_text,
                correct=correct,
                explanation=expl,
                difficulty=level,
                distractors=distractors,
                trap_map=trap_map,
                pattern_name="fraction_basics",
                subvariant=variant,
            )

        term_name = "numerator" if ask_num else "denominator"
        correct = str(num) if ask_num else str(den)
        other = str(den) if ask_num else str(num)
        q_text = f"In the fraction {num}/{den}, which number is the {term_name}?"
        candidates = [
            (other, "careless_mistake"),
            (str(num + den), "conceptual_mistake"),
            (str(den - num), "conceptual_mistake"),
            (f"1/{den}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        expl = (
            f"In any fraction a/b:\n"
            f"- 'a' (the top number) is the numerator, representing the parts taken.\n"
            f"- 'b' (the bottom number) is the denominator, representing the total equal parts.\n"
            f"Here, {num} is the numerator and {den} is the denominator. Thus, the {term_name} is {correct}."
        )

    elif variant == "division_interpretation":
        if level <= 2:
            a = random.randint(3, 7)
            b = random.randint(a + 1, 10)
            q_text = f"Which fraction represents the division expression {a} ÷ {b}?"
            correct = f"{a}/{b}"
            candidates = [
                (f"{b}/{a}", "conceptual_mistake"),
                (f"{a}/{a + b}", "formula_selection_mistake"),
                (f"{b - a}/{b}", "arithmetic_mistake"),
                (str(a * b), "conceptual_mistake"),
            ]
            distractors, trap_map = _clean_distractors(correct, candidates)
            expl = (
                f"A fraction a/b is mathematically defined as the division of the numerator by the denominator: "
                f"a ÷ b = a/b.\nTherefore, {a} ÷ {b} = {a}/{b}."
            )
        else:
            items = random.choice(["pies", "pizzas", "liters of juice", "meters of ribbon"])
            p = random.randint(4, 9)
            people = random.randint(p + 1, 15)
            q_text = (
                f"If {p} {items} are shared equally among {people} people, "
                f"what fraction of a single {items.split()[-1].rstrip('s')} does each person receive?"
            )
            correct = f"{p}/{people}"
            candidates = [
                (f"{people}/{p}", "conceptual_mistake"),
                (f"{people - p}/{people}", "careless_mistake"),
                (f"1/{people}", "formula_selection_mistake"),
                (f"{p}/{people - p}", "arithmetic_mistake"),
            ]
            distractors, trap_map = _clean_distractors(correct, candidates)
            expl = (
                f"Sharing {p} units equally among {people} people means computing {p} ÷ {people}.\n"
                f"By definition of division as a fraction, {p} ÷ {people} = {p}/{people}."
            )

    elif variant == "classify_fraction":
        types = ["proper", "improper", "mixed"]
        chosen_type = random.choice(types)
        if chosen_type == "proper":
            n = random.randint(2, 7)
            d = random.randint(n + 1, 12)
            frac_str = f"{n}/{d}"
            q_text = f"What type of fraction is {frac_str}?"
            correct = "Proper fraction"
            expl = (
                f"In {frac_str}, the numerator ({n}) is strictly less than the denominator ({d}). "
                f"A fraction where numerator < denominator is classified as a {correct}."
            )
        elif chosen_type == "improper":
            d = random.randint(3, 8)
            n = random.randint(d + 1, 17)
            frac_str = f"{n}/{d}"
            q_text = f"What type of fraction is {frac_str}?"
            correct = "Improper fraction"
            expl = (
                f"In {frac_str}, the numerator ({n}) is greater than or equal to the denominator ({d}). "
                f"A fraction where numerator ≥ denominator is classified as an {correct}."
            )
        else:
            w = random.randint(2, 5)
            n = random.randint(1, 4)
            d = random.randint(n + 1, 7)
            frac_str = f"{w} {n}/{d}"
            q_text = f"What type of number is {frac_str}?"
            correct = "Mixed number"
            expl = (
                f"{frac_str} consists of an integer whole number ({w}) combined with a proper fraction ({n}/{d}). "
                f"This form is classified as a {correct}."
            )

        all_classes = ["Proper fraction", "Improper fraction", "Mixed number", "Unit fraction"]
        candidates = [(c, "conceptual_mistake") for c in all_classes if c != correct]
        distractors, trap_map = _clean_distractors(correct, candidates)

    else:  # shaded_parts_concept
        total = random.randint(6, 16) if level <= 2 else random.randint(12, 36)
        shaded = random.randint(2, total - 2)
        unshaded = total - shaded
        ask_unshaded = random.choice([True, False])

        if ask_unshaded:
            target = unshaded
            wrong_target = shaded
            target_desc = "NOT shaded"
        else:
            target = shaded
            wrong_target = unshaded
            target_desc = "shaded"

        g = math.gcd(target, total)
        ans_num = target // g
        ans_den = total // g
        correct = _format_frac(ans_num, ans_den)

        wrong_g = math.gcd(wrong_target, total)
        wrong_opt = _format_frac(wrong_target // wrong_g, total // wrong_g)

        candidates = [
            (wrong_opt, "careless_mistake"),
            (_format_frac(target, wrong_target), "ratio_interpretation_mistake"),
            (_format_frac(1, total), "formula_selection_mistake"),
            (_format_frac(min(total, ans_num + 1), ans_den), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)

        shape = random.choice(["circle", "rectangle", "grid", "polygon"])
        q_text = (
            f"A {shape} is divided into {total} equal regions. If {shaded} regions are shaded, "
            f"what fraction of the {shape} is {target_desc}?"
        )
        expl = (
            f"Step 1: Total equal regions = {total}.\n"
            f"Step 2: Number of regions {target_desc} = {target}.\n"
            f"Step 3: The fraction is {target}/{total}.\n"
            f"Step 4: Simplifying by dividing numerator and denominator by GCD({target}, {total}) = {g} yields {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_basics",
        subvariant=variant,
    )

