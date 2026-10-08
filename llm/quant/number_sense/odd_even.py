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

def generate_odd_even_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "basic_classification",
        "operations_parity",
        "algebraic_parity",
        "gmat_parity_elimination",
        "consecutive_integers",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "basic_classification":
        # 0 is even! Integers divided by 2
        q_type = random.choice(["is_zero_even", "classify_negative", "even_definition"])
        if q_type == "is_zero_even":
            question = "In integer arithmetic, how is the number 0 classified regarding parity?"
            correct = "Even integer"
            distractors = ["Odd integer", "Neither even nor odd", "Both even and odd"]
            trap_map["Neither even nor odd"] = "conceptual_mistake"
            trap_map["Odd integer"] = "conceptual_mistake"
            explanation = (
                "An integer n is even if n = 2k for some integer k.\n"
                "For n = 0, 0 = 2 * 0, where k = 0 is an integer.\n"
                "Zero divided by 2 leaves a remainder of 0. Hence, 0 is strictly an even integer."
            )
        elif q_type == "classify_negative":
            num = -random.choice([13, 27, 41, 55, 69])
            question = f"What is the parity classification of {num}?"
            correct = "Odd integer"
            distractors = ["Even integer", "Neither even nor odd", "Non-integer"]
            trap_map["Neither even nor odd"] = "conceptual_mistake"
            explanation = (
                f"Negative integers also obey parity rules: {num} = 2 * ({num // 2}) + 1.\n"
                f"Because it is not divisible by 2, {num} is an odd integer."
            )
        else:
            question = "Which of the following numbers is an EVEN integer?"
            correct = "-4"
            distractors = ["3.0", "7", "11/2"]
            trap_map["3.0"] = "conceptual_mistake"
            trap_map["11/2"] = "conceptual_mistake"
            explanation = (
                "Evenness and oddness apply strictly to integers.\n"
                "-4 is divisible by 2 (-4 = 2 * -2), making it an even integer."
            )

    elif variant == "operations_parity":
        # Odd + Odd = Even, Odd * Even = Even, etc.
        rule = random.choice(["add_odd_odd", "add_odd_even", "mul_odd_odd", "mul_even_any"])
        if rule == "add_odd_odd":
            question = "If x and y are both odd integers, what must be the parity of (x + y)?"
            correct = "Always Even"
            distractors = ["Always Odd", "Even only if x and y are positive", "Cannot be determined"]
            trap_map["Always Odd"] = "conceptual_mistake"
            explanation = (
                "Let x = 2a + 1 and y = 2b + 1.\n"
                "x + y = (2a + 1) + (2b + 1) = 2(a + b + 1).\n"
                "Since this is a multiple of 2, Odd + Odd is ALWAYS Even."
            )
        elif rule == "add_odd_even":
            question = "If a is an even integer and b is an odd integer, what is the parity of (a - b)?"
            correct = "Always Odd"
            distractors = ["Always Even", "Even if a > b", "Cannot be determined"]
            trap_map["Always Even"] = "conceptual_mistake"
            explanation = (
                "Even - Odd = Odd.\n"
                "Subtracting an odd number from an even number changes parity, resulting in an Odd integer."
            )
        elif rule == "mul_odd_odd":
            question = "If m and n are both odd integers, what is the parity of (m * n)?"
            correct = "Always Odd"
            distractors = ["Always Even", "Even if m = n", "Depends on their signs"]
            trap_map["Always Even"] = "conceptual_mistake"
            explanation = (
                "The product of two odd integers contains no factor of 2.\n"
                "Therefore, Odd * Odd is ALWAYS Odd."
            )
        else:
            question = "If k is any integer, what is the parity of 2k + 4?"
            correct = "Always Even"
            distractors = ["Always Odd", "Odd if k is odd", "Depends on the sign of k"]
            trap_map["Odd if k is odd"] = "algebraic_parity_mistake"
            explanation = (
                "2k + 4 = 2(k + 2).\n"
                "Because the expression has a common factor of 2, it is divisible by 2 for all integers k.\n"
                "Thus, 2k + 4 is always Even."
            )

    elif variant == "algebraic_parity":
        # Given parity constraints, deduce expression parity
        c = random.choice([1, 2, 3])
        if c == 1:
            question = "If x is an even integer and y is an odd integer, which of the following expressions MUST be odd?"
            correct = "x^2 + y"
            distractors = ["x * y", "x + 2y", "x^2 + 2y"]
            trap_map["x * y"] = "conceptual_mistake"
            trap_map["x + 2y"] = "conceptual_mistake"
            explanation = (
                "Given x is even and y is odd:\n"
                "1. x^2 = Even * Even = Even.\n"
                "2. x^2 + y = Even + Odd = Odd.\n"
                "Let's test distractors: x * y = Even * Odd = Even; x + 2y = Even + Even = Even.\n"
                "Thus, x^2 + y must be odd."
            )
        elif c == 2:
            question = "If (3a + 5) is an even integer, which of the following statements must be true about integer a?"
            correct = "a must be odd"
            distractors = ["a must be even", "a can be either even or odd", "a must be a multiple of 5"]
            trap_map["a must be even"] = "conceptual_mistake"
            explanation = (
                "3a + 5 = Even => 3a = Even - 5 = Even - Odd = Odd.\n"
                "Since 3a is odd and 3 is odd, a MUST be odd (because Odd * Odd = Odd, whereas Odd * Even = Even)."
            )
        else:
            question = "If n is an integer, which of the following expressions is ALWAYS even for any value of n?"
            correct = "n^2 - n"
            distractors = ["n^2 + 1", "n^2 + n + 1", "2n + 1"]
            trap_map["n^2 + n + 1"] = "algebraic_parity_mistake"
            trap_map["2n + 1"] = "conceptual_mistake"
            explanation = (
                "Notice that n^2 - n = n(n - 1).\n"
                "Here, n and (n - 1) are two consecutive integers. In any pair of consecutive integers, "
                "one is always even and the other is odd.\n"
                "Their product must contain a factor of 2, so n^2 - n is ALWAYS even."
            )

    elif variant == "gmat_parity_elimination":
        # Data Sufficiency / Elimination drill typical of GMAT
        question = (
            "If p, q, and r are integers such that p * q * r is odd, "
            "which of the following expressions must be EVEN?"
        )
        correct = "p + q + r + 1"
        distractors = ["p + q + r", "p * q + r", "p^2 + q^2 + r^2"]
        trap_map["p + q + r"] = "conceptual_mistake"
        trap_map["p * q + r"] = "conceptual_mistake"
        explanation = (
            "If the product p * q * r is odd, none of the factors can be even.\n"
            "Therefore, p, q, and r are ALL odd integers.\n"
            "Sum of three odd integers: p + q + r = Odd + Odd + Odd = Even + Odd = Odd.\n"
            "Adding 1: (p + q + r) + 1 = Odd + 1 = Even.\n"
            "Hence, p + q + r + 1 must be even."
        )

    else:  # consecutive_integers
        num_terms = random.choice([3, 4, 5])
        if num_terms == 3:
            question = "The sum of three consecutive integers is always:"
            correct = "Divisible by 3"
            distractors = ["Divisible by 2", "Always even", "Always odd"]
            trap_map["Always even"] = "conceptual_mistake"
            trap_map["Always odd"] = "conceptual_mistake"
            explanation = (
                "Let the 3 consecutive integers be n, n+1, and n+2.\n"
                "Sum = n + (n + 1) + (n + 2) = 3n + 3 = 3(n + 1).\n"
                "This sum is a multiple of 3 regardless of whether n is even or odd."
            )
        elif num_terms == 4:
            question = "The sum of four consecutive integers is always:"
            correct = "Not divisible by 4"
            distractors = ["Divisible by 4", "An odd integer", "A prime number"]
            trap_map["Divisible by 4"] = "conceptual_mistake"
            explanation = (
                "Let four consecutive integers be n, n+1, n+2, n+3.\n"
                "Sum = 4n + 6 = 4(n + 1) + 2.\n"
                "Divided by 4, this leaves a remainder of 2. Hence, it is NEVER divisible by 4."
            )
        else:
            question = "If the product of five consecutive integers is P, which of the following must divide P?"
            correct = "120"
            distractors = ["720", "240", "48"]
            trap_map["720"] = "conceptual_mistake"
            explanation = (
                "Any sequence of k consecutive integers is always divisible by k! (k factorial).\n"
                "For 5 consecutive integers, the product is always divisible by 5! = 5 * 4 * 3 * 2 * 1 = 120."
            )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="odd_even_gmat",
        subvariant=variant,
    )

