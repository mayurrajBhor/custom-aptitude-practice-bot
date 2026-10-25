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

def generate_number_classification(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "natural_numbers",
        "whole_numbers",
        "integers_ordering",
        "signed_operations",
        "sign_determination",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "natural_numbers":
        # Concept: Natural numbers are 1, 2, 3, ... (0 is NOT natural)
        if level <= 2:
            num = random.choice([-5, -1, 0, 1, 2, 5, 12])
            is_nat = num >= 1
            correct = "Yes" if is_nat else "No"
            distractors = ["No" if is_nat else "Yes", "Only if positive", "Undefined"]
            question = f"Is the number {num} classified as a natural number (counting number)?"
            explanation = (
                f"Natural numbers are positive counting integers: {{1, 2, 3, ...}}.\n"
                f"Zero (0) is a whole number but not a natural number, and negative numbers are not natural numbers.\n"
                f"Therefore, {num} is {'a' if is_nat else 'NOT a'} natural number."
            )
            trap_map[distractors[0]] = "conceptual_mistake"
        else:
            k = random.randint(10, 30) if level <= 4 else random.randint(35, 75)
            # Sum of first k natural numbers = k*(k+1)/2
            correct_val = k * (k + 1) // 2
            wrong_zero_inc = (k - 1) * k // 2
            wrong_sq = k * k
            wrong_add = correct_val + k

            correct = str(correct_val)
            distractors = [str(wrong_zero_inc), str(wrong_sq), str(wrong_add)]
            question = f"What is the sum of the first {k} natural numbers?"
            explanation = (
                f"The sum of the first n natural numbers is given by the formula S = n(n + 1) / 2.\n"
                f"Here, n = {k}.\n"
                f"S = {k} * ({k} + 1) / 2 = {k} * {k + 1} / 2 = {correct_val}."
            )
            trap_map[str(wrong_zero_inc)] = "conceptual_mistake"
            trap_map[str(wrong_sq)] = "formula_selection_mistake"
            trap_map[str(wrong_add)] = "arithmetic_mistake"

    elif variant == "whole_numbers":
        # Whole numbers: 0, 1, 2, 3, ...
        # GMAT trap: smallest whole number is 0; negative integers are NOT whole numbers.
        q_types = ["smallest", "count_less_than", "difference_sets"]
        q_type = random.choice(q_types)
        if q_type == "smallest":
            question = "Which of the following is the smallest whole number?"
            correct = "0"
            distractors = ["1", "-1", "Does not exist"]
            trap_map["1"] = "conceptual_mistake"
            trap_map["-1"] = "conceptual_mistake"
            explanation = (
                "Whole numbers include all non-negative integers: {0, 1, 2, 3, ...}.\n"
                "The smallest whole number is 0 (natural numbers start at 1, while whole numbers include 0)."
            )
        elif q_type == "count_less_than":
            limit = random.randint(5, 20) * (level)
            correct_val = limit  # Whole numbers less than limit: 0, 1, ..., limit - 1 -> count is limit
            correct = str(correct_val)
            distractors = [str(limit - 1), str(limit + 1), str(limit - 2)]
            trap_map[str(limit - 1)] = "conceptual_mistake"  # Forgot 0
            trap_map[str(limit + 1)] = "careless_mistake"
            question = f"How many whole numbers are strictly less than {limit}?"
            explanation = (
                f"Whole numbers start at 0: {{0, 1, 2, ..., {limit - 1}}}.\n"
                f"The count of whole numbers strictly less than {limit} includes 0 up to {limit - 1}, "
                f"giving exactly {limit} numbers."
            )
        else:
            n = random.randint(10, 50)
            question = (
                f"If S is the set of all integers strictly greater than -{n} and less than {n}, "
                f"how many elements in S are whole numbers?"
            )
            # Integers: -n+1 to n-1. Whole numbers in S: 0, 1, 2, ..., n-1 -> n elements
            correct = str(n)
            distractors = [str(n - 1), str(2 * n - 1), str(n + 1)]
            trap_map[str(n - 1)] = "conceptual_mistake"  # Excluded 0
            trap_map[str(2 * n - 1)] = "careless_mistake"  # Counted all integers
            explanation = (
                f"The set S consists of integers from -{n-1} to {n-1}.\n"
                f"Whole numbers cannot be negative, so we only count elements >= 0.\n"
                f"The whole numbers in S are {{0, 1, 2, ..., {n - 1}}}, which is exactly {n} numbers."
            )

    elif variant == "integers_ordering":
        # Integers on number line, comparing negative values
        scale = 10 * level
        a = -random.randint(10, scale + 15)
        b = -random.randint(2, max(3, abs(a) - 1))
        # a < b since a is more negative
        c = random.randint(0, scale)
        # Sequence: a < b < c
        correct = f"{a} < {b} < {c}"
        distractors = [
            f"{b} < {a} < {c}",
            f"{c} < {b} < {a}",
            f"{a} < {c} < {b}",
        ]
        trap_map[f"{b} < {a} < {c}"] = "sign_mistake"
        trap_map[f"{c} < {b} < {a}"] = "conceptual_mistake"
        question = f"Which inequality correctly orders the three integers {b}, {c}, and {a} from least to greatest?"
        explanation = (
            f"On the number line, numbers increase from left to right.\n"
            f"Since |{a}| > |{b}| and both are negative, {a} lies further to the left than {b}, meaning {a} < {b}.\n"
            f"Any non-negative integer is greater than negative integers, so {b} < {c}.\n"
            f"Thus, the correct ascending order is {a} < {b} < {c}."
        )

    elif variant == "signed_operations":
        # Operations with positive and negative integers
        a = random.randint(5, 15) * (level if level <= 3 else 4)
        b = random.randint(10, 25) * (level if level <= 3 else 4)
        op = random.choice(["sub_neg", "mul_neg", "div_neg", "nested_add_sub"])
        if op == "sub_neg":
            # a - (-b) = a + b
            correct_val = a - (-b)
            wrong_sub = a - b
            wrong_neg = -(a + b)
            correct = str(correct_val)
            distractors = [str(wrong_sub), str(wrong_neg), str(b - a)]
            trap_map[str(wrong_sub)] = "sign_mistake"
            trap_map[str(wrong_neg)] = "sign_mistake"
            question = f"Evaluate the expression: {a} - (-{b})"
            explanation = (
                f"Subtracting a negative number is equivalent to adding its positive counterpart:\n"
                f"{a} - (-{b}) = {a} + {b} = {correct_val}."
            )
        elif op == "mul_neg":
            c = -random.randint(2, 6)
            # a * c = - (a * abs(c))
            correct_val = a * c
            wrong_sign = abs(correct_val)
            wrong_add = a + c
            correct = str(correct_val)
            distractors = [str(wrong_sign), str(wrong_add), str(-wrong_add)]
            trap_map[str(wrong_sign)] = "sign_mistake"
            question = f"What is the product of {a} and {c}?"
            explanation = (
                f"The product of a positive integer and a negative integer is always negative.\n"
                f"({a}) * ({c}) = -({a} * {abs(c)}) = {correct_val}."
            )
        elif op == "div_neg":
            mult = random.randint(3, 12)
            dividend = - (mult * a)
            divisor = -a
            correct_val = dividend // divisor  # positive
            wrong_sign = -correct_val
            correct = str(correct_val)
            distractors = [str(wrong_sign), str(correct_val + 1), str(wrong_sign - 1)]
            trap_map[str(wrong_sign)] = "sign_mistake"
            question = f"Evaluate: ({dividend}) / ({divisor})"
            explanation = (
                f"The quotient of two negative numbers is positive:\n"
                f"({dividend}) / ({divisor}) = +({abs(dividend)} / {abs(divisor)}) = {correct_val}."
            )
        else:
            # -a - b + (-c)
            c = random.randint(5, 20)
            correct_val = -a - b + (-c)
            wrong_sign1 = -a - b + c
            wrong_sign2 = a + b + c
            correct = str(correct_val)
            distractors = [str(wrong_sign1), str(wrong_sign2), str(wrong_sign2 - 2 * a)]
            trap_map[str(wrong_sign1)] = "sign_mistake"
            trap_map[str(wrong_sign2)] = "sign_mistake"
            question = f"Evaluate: -{a} - {b} + (-{c})"
            explanation = (
                f"All terms are negative additions:\n"
                f"-{a} - {b} + (-{c}) = -({a} + {b} + {c}) = -({a + b + c}) = {correct_val}."
            )

    else:  # sign_determination
        # GMAT favourite: determine sign of xy, x^2 y, (x-y), etc.
        case = random.choice(["even_power", "odd_power", "subtraction_sign", "product_ratio"])
        if case == "even_power":
            question = "If x < 0 and y < 0, what is the sign of x^2 * y?"
            correct = "Always Negative"
            distractors = ["Always Positive", "Zero", "Cannot be determined without values"]
            trap_map["Always Positive"] = "sign_mistake"
            explanation = (
                "Since x < 0, x^2 = (negative)^2 = positive (an even power of any non-zero number is positive).\n"
                "Since y < 0, y is negative.\n"
                "Therefore, x^2 * y = (positive) * (negative) = negative.\n"
                "The result is always negative."
            )
        elif case == "odd_power":
            question = "If a < 0 and b > 0, what is the sign of a^3 * b^2?"
            correct = "Always Negative"
            distractors = ["Always Positive", "Zero", "Depends on the magnitude of a and b"]
            trap_map["Always Positive"] = "sign_mistake"
            explanation = (
                "For a < 0, an odd power preserves the sign: a^3 = (negative)^3 = negative.\n"
                "For b > 0, b^2 = positive.\n"
                "Thus, a^3 * b^2 = (negative) * (positive) = negative."
            )
        elif case == "subtraction_sign":
            question = "If m < n < 0, which of the following expressions must be positive?"
            correct = "n - m"
            distractors = ["m - n", "m + n", "m * n - m^2"]
            trap_map["m - n"] = "sign_mistake"
            trap_map["m + n"] = "sign_mistake"
            explanation = (
                "Given m < n, subtracting m from both sides gives n - m > 0.\n"
                "Therefore, n - m must be strictly positive regardless of the fact that both are negative."
            )
        else:
            question = "If p * q > 0 and q / r < 0, what is the sign of p * r?"
            correct = "Always Negative"
            distractors = ["Always Positive", "Zero", "Could be positive or negative"]
            trap_map["Always Positive"] = "sign_mistake"
            explanation = (
                "From p * q > 0, p and q share the same sign (both positive or both negative).\n"
                "From q / r < 0, q and r have opposite signs.\n"
                "Since p has the same sign as q, p and r must also have opposite signs.\n"
                "Therefore, their product p * r is always negative."
            )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="number_classification",
        subvariant=variant,
    )

