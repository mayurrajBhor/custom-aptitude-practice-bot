import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import (
    clamp_level,
    gcd,
    get_all_divisors,
    get_prime_factors,
    is_prime,
    lcm,
    lcm_list,
    make_mcq,
)

def generate_hcf_lcm_relation_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "product_formula_find_lcm",
        "product_formula_find_missing_num",
        "find_hcf_from_product",
        "ratio_product_relation",
        "verification_drills",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "product_formula_find_lcm":
        # HCF * LCM = a * b => LCM = (a * b) / HCF
        g = random.randint(4, 15) * level
        m1, m2 = 3, 5
        a = g * m1
        b = g * m2
        ans_lcm = g * m1 * m2
        prod = a * b
        question = (
            f"The product of two positive integers is {prod}, and their Highest Common Factor (HCF) is {g}. "
            f"What is their Least Common Multiple (LCM)?"
        )
        correct = str(ans_lcm)
        distractors = [str(ans_lcm * 2), str(prod // (g * 2)), str(ans_lcm + g)]
        trap_map[str(ans_lcm * 2)] = "arithmetic_mistake"
        explanation = (
            f"Fundamental formula: HCF * LCM = Product of the two numbers.\n"
            f"{g} * LCM = {prod}\n"
            f"LCM = {prod} / {g} = {ans_lcm}."
        )

    elif variant == "product_formula_find_missing_num":
        # Given HCF, LCM, and one number, find the other number
        g = random.randint(3, 12) * level
        m1, m2 = 4, 7
        num1 = g * m1
        num2 = g * m2
        cur_lcm = g * m1 * m2
        question = (
            f"The HCF and LCM of two numbers are {g} and {cur_lcm}, respectively. "
            f"If one of the numbers is {num1}, find the other number."
        )
        correct = str(num2)
        distractors = [str(num2 + g), str(num2 - g), str(num1)]
        trap_map[str(num2 + g)] = "arithmetic_mistake"
        explanation = (
            f"Formula: Number 1 * Number 2 = HCF * LCM.\n"
            f"{num1} * Number 2 = {g} * {cur_lcm} = {g * cur_lcm}.\n"
            f"Number 2 = {g * cur_lcm} / {num1} = {num2}."
        )

    elif variant == "find_hcf_from_product":
        # Given product and LCM, find HCF
        g = random.randint(5, 16) * level
        m1, m2 = 2, 9
        a = g * m1
        b = g * m2
        cur_lcm = g * m1 * m2
        prod = a * b
        question = (
            f"The product of two numbers is {prod}, and their LCM is {cur_lcm}. "
            f"What is their HCF?"
        )
        correct = str(g)
        distractors = [str(g * 2), str(max(1, g // 2)), str(g + 2)]
        trap_map[str(g * 2)] = "arithmetic_mistake"
        explanation = (
            f"Formula: HCF = (Product of numbers) / LCM.\n"
            f"HCF = {prod} / {cur_lcm} = {g}."
        )

    elif variant == "ratio_product_relation":
        # Two numbers are in ratio r1:r2 and their HCF is h. Find their sum / LCM.
        r1, r2 = 3, 4
        h = random.randint(4, 12) * level
        ans_lcm = h * r1 * r2
        question = (
            f"Two numbers are in the ratio {r1} : {r2}. If their HCF is {h}, "
            f"what is their Least Common Multiple (LCM)?"
        )
        correct = str(ans_lcm)
        distractors = [str(ans_lcm * 2), str((r1 + r2) * h), str(r1 * r2)]
        trap_map[str((r1 + r2) * h)] = "setup_mistake"  # calculated sum instead of LCM
        trap_map[str(r1 * r2)] = "conceptual_mistake"
        explanation = (
            f"Let the numbers be {r1}x and {r2}x, where x is the common factor.\n"
            f"Since {r1} and {r2} are coprime, the HCF is x = {h}.\n"
            f"The two numbers are {r1 * h} and {r2 * h}.\n"
            f"LCM = HCF * {r1} * {r2} = {h} * {r1} * {r2} = {ans_lcm}."
        )

    else:  # verification_drills
        question = (
            "Does the relationship HCF(a, b, c) * LCM(a, b, c) = a * b * c "
            "always hold for any THREE positive integers a, b, and c?"
        )
        correct = "No, the product formula holds only for two numbers"
        distractors = [
            "Yes, it holds for any number of integers",
            "Yes, provided all three numbers are even",
            "Yes, provided the numbers are distinct",
        ]
        trap_map["Yes, it holds for any number of integers"] = "conceptual_mistake"
        explanation = (
            "The identity HCF(a, b) * LCM(a, b) = a * b holds strictly for TWO numbers.\n"
            "For three numbers, HCF(a,b,c) * LCM(a,b,c) is generally NOT equal to a * b * c.\n"
            "Example: for 2, 4, 8: HCF = 2, LCM = 8 -> Product = 16, but 2 * 4 * 8 = 64."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="hcf_lcm_relation_gmat",
        subvariant=variant,
    )

