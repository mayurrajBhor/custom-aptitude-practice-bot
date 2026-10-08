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

def generate_hcf_gcd_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "hcf_two_numbers",
        "hcf_three_numbers",
        "prime_factorization_method",
        "equal_grouping_word_problems",
        "remainder_hcf",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "hcf_two_numbers":
        g = random.randint(3, 12) * level
        mult1 = random.choice([2, 3, 5, 7])
        mult2 = random.choice([4, 9, 11, 13])
        while gcd(mult1, mult2) != 1:
            mult2 += 1
        n1 = g * mult1
        n2 = g * mult2
        correct = str(g)
        distractors = [str(g * 2), str(max(1, g // 2)), str(g + 1)]
        trap_map[str(g * 2)] = "arithmetic_mistake"
        question = f"Find the Highest Common Factor (HCF / GCD) of {n1} and {n2}."
        explanation = (
            f"Using the Euclidean Algorithm:\n"
            f"GCD({n1}, {n2}):\n"
            f"Divide larger by smaller: {max(n1, n2)} = {min(n1, n2)} * {max(n1, n2) // min(n1, n2)} + {max(n1, n2) % min(n1, n2)}.\n"
            f"Continuing yields the greatest common divisor: {g}."
        )

    elif variant == "hcf_three_numbers":
        g = random.randint(2, 8) * max(1, level - 1)
        if g == 0:
            g = 4
        m1, m2, m3 = 2, 3, 5
        n1, n2, n3 = g * m1, g * m2, g * m3
        correct = str(g)
        distractors = [str(g * 2), str(g * 3), str(max(1, g - 1))]
        trap_map[str(g * 2)] = "arithmetic_mistake"
        question = f"What is the GCD of the three numbers {n1}, {n2}, and {n3}?"
        explanation = (
            f"Find GCD({n1}, {n2}) first: GCD({n1}, {n2}) = {gcd(n1, n2)}.\n"
            f"Then find GCD({gcd(n1, n2)}, {n3}) = {g}.\n"
            f"Thus, HCF({n1}, {n2}, {n3}) = {g}."
        )

    elif variant == "prime_factorization_method":
        # HCF takes lowest power of common prime factors
        question = (
            "If A = 2^3 * 3^4 * 5^2 and B = 2^2 * 3^5 * 5 * 7, "
            "what is the Highest Common Factor (HCF) of A and B?"
        )
        correct = "2^2 * 3^4 * 5"
        distractors = [
            "2^3 * 3^5 * 5^2 * 7",
            "2^2 * 3^4",
            "2^3 * 3^4 * 5",
        ]
        trap_map["2^3 * 3^5 * 5^2 * 7"] = "conceptual_mistake"  # That's LCM!
        trap_map["2^3 * 3^4 * 5"] = "formula_selection_mistake"
        explanation = (
            "To find HCF using prime factorizations, take the MINIMUM exponent for each COMMON prime factor:\n"
            "- For prime 2: min(3, 2) = 2 -> 2^2\n"
            "- For prime 3: min(4, 5) = 4 -> 3^4\n"
            "- For prime 5: min(2, 1) = 1 -> 5^1\n"
            "- Prime 7 is not common to both.\n"
            "HCF = 2^2 * 3^4 * 5."
        )

    elif variant == "equal_grouping_word_problems":
        # Classic GMAT word problem: grouping items into equal maximum size containers/rows
        g = random.randint(4, 15) * level
        m1 = random.randint(3, 7)
        m2 = random.randint(8, 12)
        while gcd(m1, m2) != 1:
            m2 += 1
        boys = g * m1
        girls = g * m2
        question = (
            f"A teacher wants to divide {boys} boys and {girls} girls into groups such that each group "
            f"has the same number of students and each group contains only boys or only girls. "
            f"What is the GREATEST possible number of students in each group?"
        )
        correct = str(g)
        distractors = [str(g * 2), str(max(2, g // 2)), str(m1 + m2)]
        trap_map[str(m1 + m2)] = "setup_mistake"
        explanation = (
            f"The maximum group size must divide both {boys} and {girls} without remainder.\n"
            f"Therefore, we must find the HCF of {boys} and {girls}.\n"
            f"HCF({boys}, {girls}) = {g} students per group."
        )

    else:  # remainder_hcf
        # Find the largest number that divides A and B leaving remainder R
        g = random.randint(6, 18) * level
        r = random.randint(2, max(2, g - 2))
        m1 = random.randint(3, 6)
        m2 = random.randint(7, 10)
        while gcd(m1, m2) != 1:
            m2 += 1
        num1 = g * m1 + r
        num2 = g * m2 + r
        question = (
            f"What is the greatest integer that divides both {num1} and {num2} "
            f"leaving a remainder of {r} in each case?"
        )
        correct = str(g)
        distractors = [str(g * 2), str(g + r), str(max(1, g - r))]
        trap_map[str(g + r)] = "setup_mistake"
        explanation = (
            f"If the divisor leaves a remainder of {r}, it must divide exactly:\n"
            f"({num1} - {r}) = {num1 - r} and ({num2} - {r}) = {num2 - r}.\n"
            f"The greatest such integer is HCF({num1 - r}, {num2 - r}) = {g}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="hcf_gcd_gmat",
        subvariant=variant,
    )

