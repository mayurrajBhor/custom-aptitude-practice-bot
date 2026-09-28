"""
GMAT Practice Engine - Day 2: Fractions and Decimals
Patterns 5010 through 5024:
- Pattern 5010: fraction_basics
- Pattern 5011: mixed_number_conversion
- Pattern 5012: equivalent_fractions
- Pattern 5013: fraction_simplification
- Pattern 5014: fraction_comparison
- Pattern 5015: fraction_addition
- Pattern 5016: fraction_subtraction
- Pattern 5017: fraction_multiplication
- Pattern 5018: fraction_division
- Pattern 5019: fraction_of_quantity
- Pattern 5020: decimal_basics
- Pattern 5021: decimal_to_fraction
- Pattern 5022: fraction_to_decimal
- Pattern 5023: fraction_to_percentage
- Pattern 5024: decimal_to_percentage
"""

import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

from llm.gmat.common import (
    clamp_level,
    gcd,
    lcm,
    make_mcq,
    GMAT_BENCHMARK_FRACTIONS,
)


def _format_frac(n: int, d: int) -> str:
    """Formats a fraction n/d, returning integer if d == 1."""
    if d == 1:
        return str(n)
    return f"{n}/{d}"


def _format_mixed(w: int, n: int, d: int) -> str:
    """Formats whole w and proper fraction n/d as a mixed number string."""
    if w == 0:
        return _format_frac(n, d)
    if n == 0:
        return str(w)
    return f"{w} {n}/{d}"


def _clean_distractors(
    correct: str,
    candidates: List[Tuple[str, str]],
) -> Tuple[List[str], Dict[str, str]]:
    """
    Given a correct answer string and a list of (distractor_str, trap_category),
    returns a deduplicated list of non-empty distractors (excluding correct)
    and a corresponding trap_map.
    """
    correct_str = str(correct).strip()
    seen = {correct_str}
    distractors: List[str] = []
    trap_map: Dict[str, str] = {}

    for cand, trap in candidates:
        s = str(cand).strip()
        if s and s not in seen:
            seen.add(s)
            distractors.append(s)
            trap_map[s] = trap

    return distractors, trap_map


# =============================================================================
# Pattern 5010: fraction_basics
# =============================================================================
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


# =============================================================================
# Pattern 5011: mixed_number_conversion
# =============================================================================
def generate_mixed_number_conversion(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["mixed_to_improper", "improper_to_mixed"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "mixed_to_improper":
        if level <= 2:
            w = random.randint(1, 4)
            d = random.randint(2, 6)
            n = random.randint(1, d - 1)
        elif level <= 4:
            w = random.randint(4, 9)
            d = random.randint(5, 12)
            n = random.randint(1, d - 1)
        else:
            w = random.randint(11, 20)
            d = random.randint(7, 16)
            n = random.randint(1, d - 1)

        while math.gcd(n, d) > 1:
            n = random.randint(1, d - 1)

        improper_num = w * d + n
        correct = f"{improper_num}/{d}"

        candidates = [
            (f"{w * n + d}/{d}", "formula_selection_mistake"),
            (f"{w + n}/{d}", "conceptual_mistake"),
            (f"{improper_num + 1}/{d}", "arithmetic_mistake"),
            (f"{improper_num - 1}/{d}", "arithmetic_mistake"),
            (f"{d}/{improper_num}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the mixed number {w} {n}/{d} into an improper fraction."
        expl = (
            f"To convert a mixed number W n/d to an improper fraction:\n"
            f"Numerator = (Whole × Denominator) + Numerator = ({w} × {d}) + {n} = {w * d} + {n} = {improper_num}.\n"
            f"Denominator stays the same: {d}.\n"
            f"Thus, {w} {n}/{d} = {correct}."
        )

    else:  # improper_to_mixed
        if level <= 2:
            w = random.randint(1, 4)
            d = random.randint(2, 5)
            r = random.randint(1, d - 1)
        elif level <= 4:
            w = random.randint(4, 9)
            d = random.randint(5, 11)
            r = random.randint(1, d - 1)
        else:
            w = random.randint(11, 20)
            d = random.randint(7, 17)
            r = random.randint(1, d - 1)

        while math.gcd(r, d) > 1:
            r = random.randint(1, d - 1)

        m = w * d + r
        correct = f"{w} {r}/{d}"

        candidates = [
            (f"{r} {w}/{d}", "careless_mistake"),
            (f"{w + 1} {r}/{d}", "arithmetic_mistake"),
            (f"{w - 1} {r + 1}/{d}", "arithmetic_mistake"),
            (f"{w} {d - r}/{d}", "formula_selection_mistake"),
            (f"{w + r}/{d}", "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the improper fraction {m}/{d} into a mixed number."
        expl = (
            f"To convert an improper fraction M/d to a mixed number:\n"
            f"1. Divide {m} by {d}: {m} ÷ {d} = {w} with a remainder of {r} (since {w} × {d} = {w * d}, and {m} - {w * d} = {r}).\n"
            f"2. The quotient ({w}) is the whole number part, and remainder ({r}) becomes the new numerator over {d}.\n"
            f"Thus, {m}/{d} = {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="mixed_number_conversion",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5012: equivalent_fractions
# =============================================================================
def generate_equivalent_fractions(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["missing_numerator", "missing_denominator", "find_equivalent", "scale_factor"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "missing_numerator":
        if level <= 2:
            a = random.randint(2, 5)
            b = random.randint(a + 1, 9)
            k = random.randint(2, 5)
        elif level <= 4:
            a = random.randint(3, 11)
            b = random.randint(a + 1, 15)
            k = random.randint(4, 9)
        else:
            a = random.randint(8, 19)
            b = random.randint(a + 1, 25)
            k = random.randint(7, 15)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        d = b * k
        x = a * k
        correct = str(x)

        candidates = [
            (str(a + (d - b)), "conceptual_mistake"),
            (str(a * (k + 1)), "arithmetic_mistake"),
            (str(a * max(1, k - 1)), "arithmetic_mistake"),
            (str(b * k), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Find the value of x if: {a}/{b} = x/{d}"
        expl = (
            f"Step 1: Determine the scale factor between the denominators: {d} ÷ {b} = {k}.\n"
            f"Step 2: Equivalent fractions require multiplying both numerator and denominator by the same factor.\n"
            f"Step 3: Multiply the numerator by {k}: x = {a} × {k} = {x}."
        )

    elif variant == "missing_denominator":
        if level <= 2:
            a = random.randint(2, 5)
            b = random.randint(a + 1, 9)
            k = random.randint(2, 5)
        elif level <= 4:
            a = random.randint(3, 11)
            b = random.randint(a + 1, 15)
            k = random.randint(4, 9)
        else:
            a = random.randint(7, 17)
            b = random.randint(a + 1, 23)
            k = random.randint(6, 14)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        c = a * k
        x = b * k
        correct = str(x)

        candidates = [
            (str(b + (c - a)), "conceptual_mistake"),
            (str(b * (k + 1)), "arithmetic_mistake"),
            (str(b * max(1, k - 1)), "arithmetic_mistake"),
            (str(c * a), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Find the value of x if: {a}/{b} = {c}/x"
        expl = (
            f"Step 1: Determine the multiplier applied to the numerator: {c} ÷ {a} = {k}.\n"
            f"Step 2: Multiply the denominator by the same scale factor {k}: x = {b} × {k} = {x}."
        )

    elif variant == "find_equivalent":
        if level <= 2:
            a = random.randint(2, 4)
            b = random.randint(a + 1, 7)
            k = random.randint(2, 4)
        else:
            a = random.randint(3, 9)
            b = random.randint(a + 1, 13)
            k = random.randint(3, 8)

        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)

        correct = f"{a * k}/{b * k}"
        candidates = [
            (f"{a + k}/{b + k}", "conceptual_mistake"),
            (f"{a * k}/{b}", "formula_selection_mistake"),
            (f"{a}/{b * k}", "formula_selection_mistake"),
            (f"{b * k}/{a * k}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Which of the following fractions is equivalent to {a}/{b}?"
        expl = (
            f"To produce an equivalent fraction, both the numerator and denominator must be multiplied "
            f"by the exact same non-zero integer.\n"
            f"Multiplying both numerator and denominator by {k} yields ({a} × {k}) / ({b} × {k}) = {correct}.\n"
            f"Note: Adding {k} to both top and bottom (e.g. {a+k}/{b+k}) alters the fraction's value and is a common trap."
        )

    else:  # scale_factor
        a = random.randint(2, 7)
        b = random.randint(a + 1, 12)
        while math.gcd(a, b) > 1:
            a = random.randint(2, b - 1)
        k = random.randint(3, 9) if level <= 3 else random.randint(11, 25)
        c = a * k
        d = b * k
        correct = str(k)
        candidates = [
            (str(k + 1), "arithmetic_mistake"),
            (str(max(1, k - 1)), "arithmetic_mistake"),
            (str(c - a), "conceptual_mistake"),
            (str(d - b), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = (
            f"By what factor were both the numerator and denominator of {a}/{b} multiplied "
            f"to create the equivalent fraction {c}/{d}?"
        )
        expl = (
            f"Scale factor = {c} ÷ {a} = {k} (and {d} ÷ {b} = {k}).\n"
            f"Thus, the scale factor used is {k}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="equivalent_fractions",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5013: fraction_simplification
# =============================================================================
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


# =============================================================================
# Pattern 5014: fraction_comparison
# =============================================================================
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


# =============================================================================
# Pattern 5015: fraction_addition
# =============================================================================
def generate_fraction_addition(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["same_denominator", "different_denominator", "mixed_numbers_addition"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "same_denominator":
        d = random.randint(5, 12)
        a = random.randint(1, d - 2)
        b = random.randint(1, d - a)
        ans = Fraction(a + b, d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a + b, 2 * d), "conceptual_mistake"),
            (_format_frac(a + b + 1, d), "arithmetic_mistake"),
            (_format_frac(abs(a - b), d), "careless_mistake"),
            (_format_frac(a * b, d), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{d} + {b}/{d}"
        expl = (
            f"Step 1: Since the denominators are identical ({d}), add the numerators directly:\n"
            f"  {a} + {b} = {a + b}.\n"
            f"Step 2: Keep the common denominator {d}: ({a} + {b})/{d} = {a + b}/{d}.\n"
            f"Step 3: Simplify if possible: {correct}."
        )

    elif variant == "different_denominator":
        if level <= 3:
            b = random.randint(2, 6)
            d = random.randint(2, 6)
            while b == d:
                d = random.randint(2, 7)
            a = random.randint(1, b - 1)
            c = random.randint(1, d - 1)
        else:
            b = random.randint(4, 10)
            d = random.randint(4, 12)
            while b == d:
                d = random.randint(4, 14)
            a = random.randint(1, b - 1)
            c = random.randint(1, d - 1)

        f1 = Fraction(a, b)
        f2 = Fraction(c, d)
        ans = f1 + f2
        correct = _format_frac(ans.numerator, ans.denominator)

        mediant = _format_frac(a + c, b + d)
        common_lcm = math.lcm(b, d)
        candidates = [
            (mediant, "conceptual_mistake"),
            (_format_frac(a + c, b * d), "formula_selection_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(ans.numerator - 1, ans.denominator), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{b} + {c}/{d}"
        expl = (
            f"Step 1: Find the least common multiple of denominators {b} and {d}: LCM({b}, {d}) = {common_lcm}.\n"
            f"Step 2: Convert to equivalent fractions with denominator {common_lcm}:\n"
            f"  {a}/{b} = {a * (common_lcm // b)}/{common_lcm}\n"
            f"  {c}/{d} = {c * (common_lcm // d)}/{common_lcm}\n"
            f"Step 3: Add numerators: {a * (common_lcm // b)} + {c * (common_lcm // d)} = {ans.numerator * (common_lcm // ans.denominator)}.\n"
            f"Step 4: Reduce to lowest terms: {correct}.\n"
            f"Common Trap: Adding top and bottom directly ({a}+{c})/({b}+{d}) = {mediant} is incorrect."
        )

    else:  # mixed_numbers_addition
        w1 = random.randint(1, 4)
        w2 = random.randint(1, 4)
        b = random.choice([2, 3, 4, 5])
        d = random.choice([2, 3, 4, 5])
        while b == d:
            d = random.choice([2, 3, 4, 6])
        a = random.randint(1, b - 1)
        c = random.randint(1, d - 1)

        f_total = w1 + Fraction(a, b) + w2 + Fraction(c, d)
        wh = f_total.numerator // f_total.denominator
        rem = f_total.numerator % f_total.denominator
        correct = _format_mixed(wh, rem, f_total.denominator)

        candidates = [
            (_format_mixed(w1 + w2, a + c, b + d), "conceptual_mistake"),
            (_format_mixed(wh + 1, rem, f_total.denominator), "arithmetic_mistake"),
            (_format_mixed(wh - 1, rem, f_total.denominator), "arithmetic_mistake"),
            (_format_frac(f_total.numerator, f_total.denominator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {w1} {a}/{b} + {w2} {c}/{d} (express as a mixed number in simplest form)"
        expl = (
            f"Step 1: Add the whole numbers: {w1} + {w2} = {w1 + w2}.\n"
            f"Step 2: Add the fractions: {a}/{b} + {c}/{d}.\n"
            f"  LCM({b}, {d}) = {math.lcm(b, d)}.\n"
            f"  Sum of fractions = {Fraction(a, b) + Fraction(c, d)}.\n"
            f"Step 3: Combine whole number and fraction: total = {f_total} = {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_addition",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5016: fraction_subtraction
# =============================================================================
def generate_fraction_subtraction(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["same_denominator", "different_denominator", "mixed_numbers_borrowing"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "same_denominator":
        d = random.randint(5, 13)
        b = random.randint(1, d - 3)
        a = random.randint(b + 1, d - 1)
        ans = Fraction(a - b, d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a + b, d), "sign_mistake"),
            (_format_frac(a - b, 2 * d), "conceptual_mistake"),
            (_format_frac(max(1, a - b + 1), d), "arithmetic_mistake"),
            (_format_frac(b, d), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{d} - {b}/{d}"
        expl = (
            f"Step 1: Denominators are the same ({d}), so subtract numerators: {a} - {b} = {a - b}.\n"
            f"Step 2: Place over common denominator: {a - b}/{d}.\n"
            f"Step 3: Simplify if necessary: {correct}."
        )

    elif variant == "different_denominator":
        b = random.randint(2, 6)
        d = random.randint(2, 7)
        while b == d:
            d = random.randint(2, 8)
        a = random.randint(1, b - 1)
        c = random.randint(1, d - 1)

        f1 = Fraction(a, b)
        f2 = Fraction(c, d)
        if f1 < f2:
            a, c = c, a
            b, d = d, b
            f1, f2 = f2, f1
        elif f1 == f2:
            a += 1
            f1 = Fraction(a, b)

        ans = f1 - f2
        correct = _format_frac(ans.numerator, ans.denominator)
        common_lcm = math.lcm(b, d)

        candidates = [
            (_format_frac(abs(a - c), abs(b - d) if b != d else b), "conceptual_mistake"),
            (_format_frac((f1 + f2).numerator, (f1 + f2).denominator), "sign_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(abs(a - c), common_lcm), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {a}/{b} - {c}/{d}"
        expl = (
            f"Step 1: Find LCM({b}, {d}) = {common_lcm}.\n"
            f"Step 2: Express with common denominator:\n"
            f"  {a}/{b} = {a * (common_lcm // b)}/{common_lcm}\n"
            f"  {c}/{d} = {c * (common_lcm // d)}/{common_lcm}\n"
            f"Step 3: Subtract numerators: {a * (common_lcm // b)} - {c * (common_lcm // d)} = {ans.numerator * (common_lcm // ans.denominator)}.\n"
            f"Step 4: Reduce to lowest terms: {correct}."
        )

    else:  # mixed_numbers_borrowing
        # Ensure fractional part of first is smaller than second (requires borrowing)
        b = random.choice([3, 4, 5])
        d = random.choice([2, 3, 4, 6])
        while b == d:
            d = random.choice([2, 3, 5, 6])

        # Pick a/b < c/d
        if Fraction(1, b) < Fraction(1, d):
            a, c = 1, 1
        else:
            a = 1
            c = d - 1

        if Fraction(a, b) >= Fraction(c, d):
            a = 1
            c = d - 1

        w1 = random.randint(4, 7)
        w2 = random.randint(1, w1 - 2)

        total_ans = (w1 + Fraction(a, b)) - (w2 + Fraction(c, d))
        wh = total_ans.numerator // total_ans.denominator
        rem = total_ans.numerator % total_ans.denominator
        correct = _format_mixed(wh, rem, total_ans.denominator)

        # Trap: subtracting smaller from larger without borrowing: (w1 - w2) + (c/d - a/b)
        no_borrow_frac = Fraction(c, d) - Fraction(a, b)
        no_borrow_opt = _format_mixed(w1 - w2, no_borrow_frac.numerator, no_borrow_frac.denominator)

        # Trap: forgot to decrement w1 after borrowing
        forgot_dec = _format_mixed(wh + 1, rem, total_ans.denominator)

        candidates = [
            (no_borrow_opt, "formula_selection_mistake"),
            (forgot_dec, "conceptual_mistake"),
            (_format_mixed(wh, rem + 1, total_ans.denominator), "arithmetic_mistake"),
            (_format_frac(total_ans.numerator, total_ans.denominator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {w1} {a}/{b} - {w2} {c}/{d} (express as a simplified mixed number)"
        expl = (
            f"Step 1: Notice that {a}/{b} < {c}/{d}, so we must borrow 1 from the whole number {w1}.\n"
            f"Step 2: Rewrite {w1} {a}/{b} as ({w1}-1) + (1 + {a}/{b}) = {w1 - 1} {a + b}/{b}.\n"
            f"Step 3: Convert both fractional parts to common denominator {math.lcm(b, d)} and subtract:\n"
            f"  Whole numbers: {w1 - 1} - {w2} = {wh}.\n"
            f"  Fractions: {a + b}/{b} - {c}/{d} = {Fraction(a + b, b) - Fraction(c, d)}.\n"
            f"Step 4: Combined result is {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_subtraction",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5017: fraction_multiplication
# =============================================================================
def generate_fraction_multiplication(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["direct_multiplication", "cross_cancellation", "whole_times_fraction", "multiple_fractions"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "direct_multiplication":
        a = random.randint(1, 5)
        b = random.randint(a + 1, 7)
        c = random.randint(1, 5)
        d = random.randint(c + 1, 8)
        ans = Fraction(a * c, b * d)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a * d, b * c), "formula_selection_mistake"),
            (_format_frac(a + c, b + d), "conceptual_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(b * d, a * c), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Multiply: {a}/{b} × {c}/{d}"
        expl = (
            f"Step 1: Multiply numerators straight across: {a} × {c} = {a * c}.\n"
            f"Step 2: Multiply denominators straight across: {b} × {d} = {b * d}.\n"
            f"Step 3: Reduce the resulting fraction: {a * c}/{b * d} = {correct}.\n"
            f"Trap: Do not cross-multiply ({a}×{d} / {b}×{c}) when multiplying fractions."
        )

    elif variant == "cross_cancellation":
        # Fraction 1: a/b, Fraction 2: (k*b)/c, so b cancels
        b = random.choice([3, 4, 5, 7])
        k = random.choice([2, 3])
        a = random.randint(1, b - 1)
        c = random.randint(k * a + 1, max(k * a + 5, 20))
        while math.gcd(k * a, c) == c:
            c += 1

        f1 = f"{a}/{b}"
        f2 = f"{k * b}/{c}"
        ans = Fraction(a * k * b, b * c)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a * k * b, c), "conceptual_mistake"),
            (_format_frac(ans.denominator, ans.numerator), "careless_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(a * c, b * k * b), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Compute using cross-cancellation: {f1} × {f2}"
        expl = (
            f"Step 1: Look for common factors between numerators and denominators.\n"
            f"Notice that {b} in the denominator of the first fraction and {k * b} in the numerator of the second "
            f"both divide by {b}: {k * b} ÷ {b} = {k} and {b} ÷ {b} = 1.\n"
            f"Step 2: Multiply the simplified terms: ({a} × {k}) / (1 × {c}) = {a * k}/{c}.\n"
            f"Step 3: Reduce to lowest terms: {correct}."
        )

    elif variant == "whole_times_fraction":
        k = random.randint(3, 8)
        b = random.randint(3, 7)
        a = random.randint(1, b - 1)
        ans = Fraction(k * a, b)
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (_format_frac(a, b), "conceptual_mistake"),
            (_format_frac(a, k * b), "formula_selection_mistake"),
            (_format_frac(k * a + 1, b), "arithmetic_mistake"),
            (_format_frac(k + a, b), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: {k} × {a}/{b}"
        expl = (
            f"Step 1: Express the integer {k} as a fraction: {k}/1.\n"
            f"Step 2: Multiply numerators and denominators: ({k} × {a}) / (1 × {b}) = {k * a}/{b}.\n"
            f"Step 3: Simplify: {correct}.\n"
            f"Trap: Do NOT multiply both numerator and denominator by {k} (e.g. {k*a}/{k*b} = {a}/{b})."
        )

    else:  # multiple_fractions
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 3)
        f3 = Fraction(3, 5)
        ans = f1 * f2 * f3
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            ("1/2", "arithmetic_mistake"),
            ("6/30", "conceptual_mistake"),
            ("2/5", "arithmetic_mistake"),
            ("1/3", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Calculate the product: (1/2) × (2/3) × (3/5)"
        expl = (
            f"Step 1: Cancel common factors across numerators and denominators:\n"
            f"  - The 2 in the denominator of (1/2) cancels with the 2 in the numerator of (2/3).\n"
            f"  - The 3 in the denominator of (2/3) cancels with the 3 in the numerator of (3/5).\n"
            f"Step 2: The remaining product is (1 × 1 × 1) / (1 × 1 × 5) = 1/5."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_multiplication",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5018: fraction_division
# =============================================================================
def generate_fraction_division(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["keep_change_flip", "whole_and_fraction", "mixed_numbers_division"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "keep_change_flip":
        a = random.randint(2, 5)
        b = random.randint(a + 1, 9)
        c = random.randint(2, 5)
        d = random.randint(c + 1, 9)
        while a * d == b * c:
            d += 1

        ans = Fraction(a * d, b * c)
        correct = _format_frac(ans.numerator, ans.denominator)

        mult_direct = Fraction(a * c, b * d)
        flip_first = Fraction(b * c, a * d)
        flip_both = Fraction(b * d, a * c)

        candidates = [
            (_format_frac(mult_direct.numerator, mult_direct.denominator), "formula_selection_mistake"),
            (_format_frac(flip_first.numerator, flip_first.denominator), "formula_selection_mistake"),
            (_format_frac(flip_both.numerator, flip_both.denominator), "conceptual_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: ({a}/{b}) ÷ ({c}/{d})"
        expl = (
            f"To divide by a fraction, use the 'Keep-Change-Flip' rule:\n"
            f"1. KEEP the first fraction: {a}/{b}\n"
            f"2. CHANGE division (÷) to multiplication (×)\n"
            f"3. FLIP the divisor to its reciprocal: {d}/{c}\n"
            f"Now multiply: ({a}/{b}) × ({d}/{c}) = ({a} × {d}) / ({b} × {c}) = {a * d}/{b * c}.\n"
            f"Simplified: {correct}."
        )

    elif variant == "whole_and_fraction":
        divide_whole_by_frac = random.choice([True, False])
        if divide_whole_by_frac:
            k = random.randint(3, 8)
            b = random.randint(3, 6)
            a = random.randint(1, b - 1)
            ans = Fraction(k * b, a)
            correct = _format_frac(ans.numerator, ans.denominator)
            q_text = f"Calculate: {k} ÷ ({a}/{b})"
            candidates = [
                (_format_frac(k * a, b), "formula_selection_mistake"),
                (_format_frac(a, k * b), "conceptual_mistake"),
                (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
                (str(k * b), "careless_mistake"),
            ]
            expl = (
                f"Step 1: Write {k} as {k}/1.\n"
                f"Step 2: Flip the second fraction to {b}/{a} and multiply: ({k}/1) × ({b}/{a}) = {k * b}/{a}.\n"
                f"Step 3: Simplify: {correct}."
            )
        else:
            b = random.randint(3, 7)
            a = random.randint(1, b - 1)
            k = random.randint(2, 6)
            ans = Fraction(a, b * k)
            correct = _format_frac(ans.numerator, ans.denominator)
            q_text = f"Calculate: ({a}/{b}) ÷ {k}"
            candidates = [
                (_format_frac(a * k, b), "formula_selection_mistake"),
                (_format_frac(b * k, a), "conceptual_mistake"),
                (_format_frac(ans.numerator, ans.denominator + 1), "arithmetic_mistake"),
            ]
            expl = (
                f"Step 1: The reciprocal of integer {k} is 1/{k}.\n"
                f"Step 2: Multiply ({a}/{b}) × (1/{k}) = {a}/{b * k}.\n"
                f"Step 3: Simplify: {correct}."
            )
        distractors, trap_map = _clean_distractors(correct, candidates)

    else:  # mixed_numbers_division
        w1 = random.randint(2, 4)
        w2 = random.randint(1, 2)
        f1 = w1 + Fraction(1, 2)
        f2 = w2 + Fraction(1, 4)
        ans = f1 / f2
        correct = _format_frac(ans.numerator, ans.denominator)

        candidates = [
            (str(w1 // w2), "conceptual_mistake"),
            (_format_frac((f1 * f2).numerator, (f1 * f2).denominator), "formula_selection_mistake"),
            (_format_frac(ans.numerator + 1, ans.denominator), "arithmetic_mistake"),
            (_format_frac(ans.denominator, ans.numerator), "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Calculate: ({w1} 1/2) ÷ ({w2} 1/4)"
        expl = (
            f"Step 1: Convert both mixed numbers into improper fractions:\n"
            f"  {w1} 1/2 = {f1.numerator}/{f1.denominator}\n"
            f"  {w2} 1/4 = {f2.numerator}/{f2.denominator}\n"
            f"Step 2: Multiply by the reciprocal of the second fraction:\n"
            f"  ({f1.numerator}/{f1.denominator}) × ({f2.denominator}/{f2.numerator}) = {f1.numerator * f2.denominator}/{f1.denominator * f2.numerator}\n"
            f"Step 3: Simplify to lowest terms: {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_division",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5019: fraction_of_quantity
# =============================================================================
def generate_fraction_of_quantity(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["direct_quantity", "word_problem", "reverse_quantity"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "direct_quantity":
        if level <= 2:
            den = random.choice([3, 4, 5, 8, 10])
            num = random.randint(1, den - 1)
            k = random.randint(5, 15)
        elif level <= 4:
            den = random.choice([6, 7, 8, 12, 15])
            num = random.randint(2, den - 1)
            k = random.randint(10, 30)
        else:
            den = random.choice([11, 13, 14, 16, 20])
            num = random.randint(3, den - 1)
            k = random.randint(20, 50)

        total = k * den
        ans = k * num
        correct = str(ans)

        candidates = [
            (str(ans + k), "arithmetic_mistake"),
            (str(ans - k), "arithmetic_mistake"),
            (str(total - ans), "careless_mistake"),
            (str((total // num) * den if num > 0 else total), "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is {num}/{den} of {total}?"
        expl = (
            f"Step 1: Divide the quantity by the denominator to find 1 part: {total} ÷ {den} = {k}.\n"
            f"Step 2: Multiply by the numerator: {k} × {num} = {ans}.\n"
            f"Thus, {num}/{den} of {total} is {correct}."
        )

    elif variant == "word_problem":
        items = random.choice(["books", "laptops", "scholarship funds", "candies", "tickets"])
        den = random.choice([4, 5, 8, 10])
        num = random.randint(1, den - 1)
        k = random.randint(10, 40)
        total = k * den

        used_qty = num * k
        remaining_qty = total - used_qty
        correct = str(remaining_qty)

        candidates = [
            (str(used_qty), "careless_mistake"),
            (str(remaining_qty + k), "arithmetic_mistake"),
            (str(remaining_qty - k), "arithmetic_mistake"),
            (str(total - num), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = (
            f"A school library received an inventory of {total} {items}. "
            f"During the first week, {num}/{den} of the total {items} were checked out. "
            f"How many {items} REMAIN in the library?"
        )
        expl = (
            f"Step 1: Calculate the quantity checked out: ({num}/{den}) × {total} = {num} × {k} = {used_qty}.\n"
            f"Step 2: Subtract the checked-out items from the total inventory: {total} - {used_qty} = {remaining_qty}.\n"
            f"Common Trap: Answering {used_qty} answers how many were checked out, not how many remain!"
        )

    else:  # reverse_quantity
        den = random.choice([3, 4, 5, 7, 8])
        num = random.randint(2, den - 1)
        k = random.randint(6, 18)
        part = k * num
        original = k * den
        correct = str(original)

        candidates = [
            (str(part * num // den), "formula_selection_mistake"),
            (str(part * den), "conceptual_mistake"),
            (str(original + den), "arithmetic_mistake"),
            (str(original - den), "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"If {num}/{den} of a mystery number is {part}, what is the original number?"
        expl = (
            f"Step 1: Set up the equation: ({num}/{den}) × N = {part}.\n"
            f"Step 2: Solve for N by multiplying both sides by the reciprocal {den}/{num}:\n"
            f"  N = {part} × ({den}/{num}) = ({part} ÷ {num}) × {den} = {k} × {den} = {original}.\n"
            f"Thus, the original number is {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_of_quantity",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5020: decimal_basics
# =============================================================================
def generate_decimal_basics(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["place_value", "comparing_decimals", "ordering_decimals"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "place_value":
        d1 = random.randint(1, 9)
        d2 = random.randint(1, 9)
        d3 = random.randint(1, 9)
        d4 = random.randint(1, 9)
        num_str = f"3.{d1}{d2}{d3}{d4}"

        places = [
            (d1, "Tenths (0.1)"),
            (d2, "Hundredths (0.01)"),
            (d3, "Thousandths (0.001)"),
            (d4, "Ten-thousandths (0.0001)"),
        ]
        target_digit, correct = random.choice(places)

        all_names = ["Tenths (0.1)", "Hundredths (0.01)", "Thousandths (0.001)", "Ten-thousandths (0.0001)"]
        candidates = [(name, "conceptual_mistake") for name in all_names if name != correct]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"In the number {num_str}, what is the place value of the digit {target_digit}?"
        expl = (
            f"In decimal place notation to the right of the decimal point:\n"
            f"- 1st place = Tenths (0.1)\n"
            f"- 2nd place = Hundredths (0.01)\n"
            f"- 3rd place = Thousandths (0.001)\n"
            f"- 4th place = Ten-thousandths (0.0001)\n"
            f"Here, {target_digit} is in the {correct.split()[0].lower()} position."
        )

    elif variant == "comparing_decimals":
        # The classic trap: longer decimals are not necessarily larger!
        decimals = ["0.08", "0.8", "0.088", "0.0089"]
        correct = "0.8"
        candidates = [
            ("0.088", "conceptual_mistake"),
            ("0.0089", "conceptual_mistake"),
            ("0.08", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Which of the following decimals has the greatest numerical value?"
        expl = (
            f"To compare decimals, align them by the decimal point or pad with trailing zeros:\n"
            f"  0.0800\n"
            f"  0.8000  <-- largest (8 tenths)\n"
            f"  0.0880\n"
            f"  0.0089\n"
            f"0.8 has 8 tenths, whereas all other choices have 0 tenths. "
            f"Common Trap: Believing 0.0089 is larger because 89 is a bigger number is incorrect."
        )

    else:  # ordering_decimals
        decimals = [0.05, 0.5, 0.055, 0.505]
        decimals_sorted = sorted(decimals)
        correct = " < ".join(str(x) for x in decimals_sorted)
        reversed_order = " < ".join(str(x) for x in reversed(decimals_sorted))

        candidates = [
            (reversed_order, "careless_mistake"),
            ("0.05 < 0.5 < 0.055 < 0.505", "conceptual_mistake"),
            ("0.055 < 0.05 < 0.5 < 0.505", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = "Which of the following arranges the decimals 0.5, 0.05, 0.505, and 0.055 in ascending order?"
        expl = (
            f"Padding each decimal to 3 places:\n"
            f"  0.050, 0.055, 0.500, 0.505\n"
            f"Ordering from smallest to largest yields {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_basics",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5021: decimal_to_fraction
# =============================================================================
def generate_decimal_to_fraction(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["terminating_one_place", "terminating_two_places", "terminating_three_places", "mixed_decimal"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "terminating_one_place":
        dec_val = random.choice([0.2, 0.4, 0.6, 0.8])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(dec_val * 10)}/10", "conceptual_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"1/{int(dec_val * 10)}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the terminating decimal {dec_val} into a simplified fraction."
        expl = (
            f"Step 1: Write {dec_val} over 10: {int(dec_val * 10)}/10.\n"
            f"Step 2: Simplify by dividing numerator and denominator by 2: {correct}."
        )

    elif variant == "terminating_two_places":
        dec_val = random.choice([0.15, 0.25, 0.35, 0.45, 0.65, 0.75, 0.85, 0.64])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(round(dec_val * 100))}/100", "conceptual_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"{frac.numerator}/{frac.denominator + 5}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a fraction in lowest terms."
        expl = (
            f"Step 1: Express as a fraction over 100: {int(round(dec_val * 100))}/100.\n"
            f"Step 2: Divide both terms by their GCD ({math.gcd(int(round(dec_val * 100)), 100)}):\n"
            f"  {int(round(dec_val * 100))}/100 = {correct}."
        )

    elif variant == "terminating_three_places":
        dec_val = random.choice([0.125, 0.375, 0.625, 0.875, 0.048, 0.064])
        frac = Fraction(str(dec_val))
        correct = _format_frac(frac.numerator, frac.denominator)

        candidates = [
            (f"{int(round(dec_val * 1000))}/1000", "conceptual_mistake"),
            (f"{frac.numerator}/{frac.denominator * 2}", "formula_selection_mistake"),
            (f"{frac.numerator + 1}/{frac.denominator}", "arithmetic_mistake"),
            (f"{frac.denominator}/{frac.numerator}", "careless_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a simplified fraction."
        expl = (
            f"Step 1: Write as a fraction over 1,000: {int(round(dec_val * 1000))}/1000.\n"
            f"Step 2: Reduce by dividing by the GCD: {correct}."
        )

    else:  # mixed_decimal
        dec_val = random.choice([1.25, 1.75, 2.5, 3.2, 2.125])
        frac = Fraction(str(dec_val))
        wh = frac.numerator // frac.denominator
        rem = frac.numerator % frac.denominator
        correct = _format_mixed(wh, rem, frac.denominator)

        candidates = [
            (_format_frac(frac.numerator, frac.denominator), "careless_mistake"),
            (_format_mixed(wh + 1, rem, frac.denominator), "arithmetic_mistake"),
            (_format_mixed(wh, rem + 1, frac.denominator), "arithmetic_mistake"),
            (_format_mixed(wh, int((dec_val - wh) * 100), 100), "conceptual_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {dec_val} into a mixed number in simplest form."
        expl = (
            f"Step 1: The whole number part is {wh}.\n"
            f"Step 2: The decimal part is {round(dec_val - wh, 3)} = {rem}/{frac.denominator} in lowest terms.\n"
            f"Step 3: Combine to get the mixed number: {correct}."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_to_fraction",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5022: fraction_to_decimal
# =============================================================================
def generate_fraction_to_decimal(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["terminating_benchmark", "terminating_advanced", "recurring_fractions"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "terminating_benchmark":
        benchmarks = [
            (1, 2, "0.5"),
            (1, 4, "0.25"),
            (3, 4, "0.75"),
            (1, 5, "0.2"),
            (2, 5, "0.4"),
            (3, 5, "0.6"),
            (4, 5, "0.8"),
            (1, 8, "0.125"),
            (3, 8, "0.375"),
            (5, 8, "0.625"),
            (7, 8, "0.875"),
        ]
        n, d, correct = random.choice(benchmarks)
        val = float(correct)
        candidates = [
            (f"{val + 0.05:.3g}", "arithmetic_mistake"),
            (f"{val - 0.05:.3g}", "arithmetic_mistake"),
            (f"0.{n}{d}", "conceptual_mistake"),
            (f"{val * 10:.3g}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is the decimal equivalent of the fraction {n}/{d}?"
        expl = (
            f"To convert {n}/{d} to a decimal, divide {n} by {d}:\n"
            f"  {n} ÷ {d} = {correct}.\n"
            f"Benchmark recall: {n}/{d} is a standard GMAT benchmark fraction equal to {correct}."
        )

    elif variant == "terminating_advanced":
        advanced = [
            (1, 16, "0.0625"),
            (3, 16, "0.1875"),
            (7, 20, "0.35"),
            (9, 20, "0.45"),
            (11, 25, "0.44"),
            (7, 40, "0.175"),
            (13, 50, "0.26"),
        ]
        n, d, correct = random.choice(advanced)
        val = float(correct)
        candidates = [
            (f"{val / 10:.4g}", "conceptual_mistake"),
            (f"{val * 10:.4g}", "conceptual_mistake"),
            (f"{val + 0.02:.4g}", "arithmetic_mistake"),
            (f"{val - 0.02:.4g}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the fraction {n}/{d} into a terminating decimal."
        expl = (
            f"Divide {n} by {d}:\n"
            f"  {n} ÷ {d} = {correct}."
        )

    else:  # recurring_fractions
        recurring = [
            (1, 3, "0.333...", ["0.3", "0.33", "0.0333..."]),
            (2, 3, "0.666...", ["0.6", "0.66", "0.0666..."]),
            (1, 6, "0.1666...", ["0.16", "0.6", "0.0166..."]),
            (5, 6, "0.8333...", ["0.83", "0.8", "0.0833..."]),
            (1, 9, "0.111...", ["0.1", "0.0111...", "0.9"]),
        ]
        n, d, correct, wrong_opts = random.choice(recurring)
        candidates = [(w, "conceptual_mistake") for w in wrong_opts]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is the recurring decimal value of {n}/{d}?"
        expl = (
            f"Dividing {n} by {d} yields a repeating (recurring) decimal:\n"
            f"  {n} ÷ {d} = {correct}\n"
            f"Note: Terminating values like {wrong_opts[0]} are rough approximations, not exact representations."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_to_decimal",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5023: fraction_to_percentage
# =============================================================================
def generate_fraction_to_percentage(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["fraction_to_percent", "percent_to_fraction", "improper_fraction_to_percent"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    benchmarks = [
        (1, 2, "50%"),
        (1, 3, "33.33%"),
        (2, 3, "66.67%"),
        (1, 4, "25%"),
        (3, 4, "75%"),
        (1, 5, "20%"),
        (2, 5, "40%"),
        (3, 5, "60%"),
        (4, 5, "80%"),
        (1, 6, "16.67%"),
        (5, 6, "83.33%"),
        (1, 8, "12.5%"),
        (3, 8, "37.5%"),
        (5, 8, "62.5%"),
        (7, 8, "87.5%"),
        (1, 10, "10%"),
    ]

    if variant == "fraction_to_percent":
        n, d, pct = random.choice(benchmarks)
        correct = pct
        val = float(pct.replace("%", ""))

        candidates = [
            (f"{val / 10:.2f}%", "conceptual_mistake"),
            (f"{val * 10:.1f}%", "conceptual_mistake"),
            (f"{val + 5:.2f}%".replace(".00%", "%"), "arithmetic_mistake"),
            ("14.28%" if pct != "14.28%" else "12.5%", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the benchmark fraction {n}/{d} into a percentage."
        expl = (
            f"Step 1: Multiply the fraction by 100%:\n"
            f"  ({n}/{d}) × 100% = {n * 100}/{d}% = {correct}.\n"
            f"Memorizing benchmark fractions ({n}/{d} = {correct}) is essential for GMAT quant speed."
        )

    elif variant == "percent_to_fraction":
        n, d, pct = random.choice(benchmarks)
        correct = f"{n}/{d}"

        candidates = [
            (f"{d}/{n}", "careless_mistake"),
            (f"{n + 1}/{d}", "arithmetic_mistake"),
            (f"{n}/{d + 1}", "arithmetic_mistake"),
            (f"{n}/{d * 2}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {pct} into a fraction in simplest terms."
        expl = (
            f"Step 1: Express {pct} as a fraction over 100.\n"
            f"Step 2: Recognize the benchmark table equivalent: {pct} = {correct}."
        )

    else:  # improper_fraction_to_percent
        impropers = [
            (5, 4, "125%"),
            (3, 2, "150%"),
            (7, 5, "140%"),
            (4, 3, "133.33%"),
            (9, 8, "112.5%"),
        ]
        n, d, correct = random.choice(impropers)
        val = float(correct.replace("%", ""))
        candidates = [
            (f"{val - 100}%", "careless_mistake"),
            (f"{val / 10}%", "conceptual_mistake"),
            (f"{val + 10}%", "arithmetic_mistake"),
            ("100%", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the improper fraction {n}/{d} into a percentage."
        expl = (
            f"Step 1: Multiply by 100%: ({n}/{d}) × 100% = {n * 100}/{d}% = {correct}.\n"
            f"Notice that since {n} > {d}, the percentage must exceed 100%."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_to_percentage",
        subvariant=variant,
    )


# =============================================================================
# Pattern 5024: decimal_to_percentage
# =============================================================================
def generate_decimal_to_percentage(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["decimal_to_percent", "percent_to_decimal", "small_and_large_percents"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "decimal_to_percent":
        dec_val = random.choice([0.45, 0.08, 0.375, 0.025, 0.72, 0.05])
        pct_val = dec_val * 100
        correct = f"{pct_val:g}%"

        candidates = [
            (f"{pct_val / 10:g}%", "conceptual_mistake"),
            (f"{pct_val * 10:g}%", "conceptual_mistake"),
            (f"{dec_val:g}%", "formula_selection_mistake"),
            (f"{pct_val + 1:g}%", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the decimal {dec_val} into a percentage."
        expl = (
            f"To convert a decimal to a percentage, multiply by 100 (shift decimal point 2 places right):\n"
            f"  {dec_val} × 100% = {correct}."
        )

    elif variant == "percent_to_decimal":
        pct_num = random.choice([65, 7.5, 4.25, 125, 8, 3.5])
        dec_val = pct_num / 100
        correct = f"{dec_val:g}"

        candidates = [
            (f"{dec_val * 10:g}", "conceptual_mistake"),
            (f"{dec_val / 10:g}", "conceptual_mistake"),
            (f"{pct_num * 100:g}", "formula_selection_mistake"),
            (f"{dec_val + 0.01:g}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {pct_num}% into a decimal."
        expl = (
            f"To convert a percentage to a decimal, divide by 100 (shift decimal point 2 places left):\n"
            f"  {pct_num}% ÷ 100 = {correct}."
        )

    else:  # small_and_large_percents
        is_small = random.choice([True, False])
        if is_small:
            pct_num = random.choice([0.05, 0.2, 0.08, 0.4])
            dec_val = pct_num / 100
            correct = f"{dec_val:.6g}"
            candidates = [
                (f"{pct_num:.4g}", "conceptual_mistake"),
                (f"{pct_num / 10:.4g}", "conceptual_mistake"),
                (f"{pct_num * 10:.4g}", "formula_selection_mistake"),
            ]
            q_text = f"Convert {pct_num}% into a decimal."
            expl = (
                f"Dividing by 100 shifts the decimal point two places to the left:\n"
                f"  {pct_num}% ÷ 100 = {correct}."
            )
        else:
            pct_num = random.choice([250, 320, 450, 180])
            dec_val = pct_num / 100
            correct = f"{dec_val:g}"
            candidates = [
                (f"{dec_val * 10:g}", "conceptual_mistake"),
                (f"{dec_val / 10:g}", "conceptual_mistake"),
                (f"{pct_num:g}", "careless_mistake"),
            ]
            q_text = f"Convert {pct_num}% into a decimal."
            expl = (
                f"Dividing by 100 shifts the decimal point two places to the left:\n"
                f"  {pct_num}% ÷ 100 = {correct}."
            )
        distractors, trap_map = _clean_distractors(correct, candidates)

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="decimal_to_percentage",
        subvariant=variant,
    )


# =============================================================================
# Aliases and Registries
# =============================================================================
fraction_basics = generate_fraction_basics
mixed_number_conversion = generate_mixed_number_conversion
equivalent_fractions = generate_equivalent_fractions
fraction_simplification = generate_fraction_simplification
fraction_comparison = generate_fraction_comparison
fraction_addition = generate_fraction_addition
fraction_subtraction = generate_fraction_subtraction
fraction_multiplication = generate_fraction_multiplication
fraction_division = generate_fraction_division
fraction_of_quantity = generate_fraction_of_quantity
decimal_basics = generate_decimal_basics
decimal_to_fraction = generate_decimal_to_fraction
fraction_to_decimal = generate_fraction_to_decimal
fraction_to_percentage = generate_fraction_to_percentage
decimal_to_percentage = generate_decimal_to_percentage

DAY2_PATTERNS_METADATA: Dict[Union[int, str], Dict[str, Any]] = {
    5010: {
        "id": 5010,
        "name": "fraction_basics",
        "description": "Understanding numerator, denominator, division interpretation, and proper/improper/mixed fraction identification.",
        "variants": ["identify_terms", "division_interpretation", "classify_fraction", "shaded_parts_concept"],
    },
    5011: {
        "id": 5011,
        "name": "mixed_number_conversion",
        "description": "Converting mixed numbers to improper fractions (Ac+b)/c and improper fractions to mixed numbers.",
        "variants": ["mixed_to_improper", "improper_to_mixed"],
    },
    5012: {
        "id": 5012,
        "name": "equivalent_fractions",
        "description": "Finding equivalent fractions, missing numerators/denominators (e.g. 3/5 = x/20), and scale factor identification.",
        "variants": ["missing_numerator", "missing_denominator", "find_equivalent", "scale_factor"],
    },
    5013: {
        "id": 5013,
        "name": "fraction_simplification",
        "description": "Reducing fractions to lowest terms, identifying already simplified fractions, and using the GCD.",
        "variants": ["reduce_lowest_terms", "identify_simplified", "gcd_simplification"],
    },
    5014: {
        "id": 5014,
        "name": "fraction_comparison",
        "description": "Comparing fractions with like denominators, like numerators, cross-multiplication, and ordering sets of fractions.",
        "variants": ["same_denominator", "same_numerator", "cross_multiplication", "ordering"],
    },
    5015: {
        "id": 5015,
        "name": "fraction_addition",
        "description": "Adding fractions with same or different denominators using LCM, and adding mixed numbers.",
        "variants": ["same_denominator", "different_denominator", "mixed_numbers_addition"],
    },
    5016: {
        "id": 5016,
        "name": "fraction_subtraction",
        "description": "Subtracting fractions with same or different denominators, and subtracting mixed numbers with borrowing.",
        "variants": ["same_denominator", "different_denominator", "mixed_numbers_borrowing"],
    },
    5017: {
        "id": 5017,
        "name": "fraction_multiplication",
        "description": "Direct fraction multiplication, cross-cancellation, whole number times fraction, and chaining multiple fractions.",
        "variants": ["direct_multiplication", "cross_cancellation", "whole_times_fraction", "multiple_fractions"],
    },
    5018: {
        "id": 5018,
        "name": "fraction_division",
        "description": "Dividing fractions using keep-change-flip (a/b * d/c), whole numbers with fractions, and mixed number division.",
        "variants": ["keep_change_flip", "whole_and_fraction", "mixed_numbers_division"],
    },
    5019: {
        "id": 5019,
        "name": "fraction_of_quantity",
        "description": "Calculating fractions of quantities (e.g. 3/5 of 100), word problems with remaining amounts, and reverse quantity problems.",
        "variants": ["direct_quantity", "word_problem", "reverse_quantity"],
    },
    5020: {
        "id": 5020,
        "name": "decimal_basics",
        "description": "Understanding tenths, hundredths, thousandths place values, and comparing and ordering decimals.",
        "variants": ["place_value", "comparing_decimals", "ordering_decimals"],
    },
    5021: {
        "id": 5021,
        "name": "decimal_to_fraction",
        "description": "Converting terminating decimals (one, two, or three decimal places) and mixed decimals to simplified fractions.",
        "variants": ["terminating_one_place", "terminating_two_places", "terminating_three_places", "mixed_decimal"],
    },
    5022: {
        "id": 5022,
        "name": "fraction_to_decimal",
        "description": "Converting terminating fractions (1/2, 1/4, 1/8, 1/5) and recurring fractions (1/3, 1/6) to decimals.",
        "variants": ["terminating_benchmark", "terminating_advanced", "recurring_fractions"],
    },
    5023: {
        "id": 5023,
        "name": "fraction_to_percentage",
        "description": "Conversions both ways between fractions and percentages using the benchmark table, including improper fractions.",
        "variants": ["fraction_to_percent", "percent_to_fraction", "improper_fraction_to_percent"],
    },
    5024: {
        "id": 5024,
        "name": "decimal_to_percentage",
        "description": "Conversions between decimals and percentages (decimal * 100 = %, % / 100 = decimal), including small and large percentages.",
        "variants": ["decimal_to_percent", "percent_to_decimal", "small_and_large_percents"],
    },
}

# Also support name-based and str-based lookups in DAY2_PATTERNS_METADATA
for _pid in list(DAY2_PATTERNS_METADATA.keys()):
    _data = DAY2_PATTERNS_METADATA[_pid]
    DAY2_PATTERNS_METADATA[str(_pid)] = _data
    DAY2_PATTERNS_METADATA[_data["name"]] = _data

DAY2_GENERATORS: Dict[Union[int, str], Any] = {
    5010: generate_fraction_basics,
    "5010": generate_fraction_basics,
    "fraction_basics": generate_fraction_basics,

    5011: generate_mixed_number_conversion,
    "5011": generate_mixed_number_conversion,
    "mixed_number_conversion": generate_mixed_number_conversion,

    5012: generate_equivalent_fractions,
    "5012": generate_equivalent_fractions,
    "equivalent_fractions": generate_equivalent_fractions,

    5013: generate_fraction_simplification,
    "5013": generate_fraction_simplification,
    "fraction_simplification": generate_fraction_simplification,

    5014: generate_fraction_comparison,
    "5014": generate_fraction_comparison,
    "fraction_comparison": generate_fraction_comparison,

    5015: generate_fraction_addition,
    "5015": generate_fraction_addition,
    "fraction_addition": generate_fraction_addition,

    5016: generate_fraction_subtraction,
    "5016": generate_fraction_subtraction,
    "fraction_subtraction": generate_fraction_subtraction,

    5017: generate_fraction_multiplication,
    "5017": generate_fraction_multiplication,
    "fraction_multiplication": generate_fraction_multiplication,

    5018: generate_fraction_division,
    "5018": generate_fraction_division,
    "fraction_division": generate_fraction_division,

    5019: generate_fraction_of_quantity,
    "5019": generate_fraction_of_quantity,
    "fraction_of_quantity": generate_fraction_of_quantity,

    5020: generate_decimal_basics,
    "5020": generate_decimal_basics,
    "decimal_basics": generate_decimal_basics,

    5021: generate_decimal_to_fraction,
    "5021": generate_decimal_to_fraction,
    "decimal_to_fraction": generate_decimal_to_fraction,

    5022: generate_fraction_to_decimal,
    "5022": generate_fraction_to_decimal,
    "fraction_to_decimal": generate_fraction_to_decimal,

    5023: generate_fraction_to_percentage,
    "5023": generate_fraction_to_percentage,
    "fraction_to_percentage": generate_fraction_to_percentage,

    5024: generate_decimal_to_percentage,
    "5024": generate_decimal_to_percentage,
    "decimal_to_percentage": generate_decimal_to_percentage,
}
