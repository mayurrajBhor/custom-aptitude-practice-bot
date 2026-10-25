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

def generate_order_of_operations_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "bodmas_basic",
        "nested_parentheses",
        "mult_div_left_right",
        "signed_bodmas",
        "tricky_gmat_expressions",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "bodmas_basic":
        # a + b * c - d / e
        b = random.randint(3, 8)
        c = random.randint(2, 6)
        e = random.randint(2, 5)
        d = e * random.randint(2, 6)
        a = random.randint(10, 30)
        # a + (b * c) - (d // e)
        correct_val = a + (b * c) - (d // e)
        # Trap: (a + b) * c - d / e
        wrong_left_to_right = (a + b) * c - (d // e)
        # Trap: add before mult
        wrong_add = correct_val + 2
        correct = str(correct_val)
        distractors = [str(wrong_left_to_right), str(wrong_add), str(correct_val - 4)]
        trap_map[str(wrong_left_to_right)] = "formula_selection_mistake"
        question = f"Evaluate the expression: {a} + {b} * {c} - {d} / {e}"
        explanation = (
            f"Follow BODMAS (Brackets, Orders, Division/Multiplication, Addition/Subtraction):\n"
            f"1. Perform Division and Multiplication first:\n"
            f"   {b} * {c} = {b * c}\n"
            f"   {d} / {e} = {d // e}\n"
            f"2. Perform Addition and Subtraction left to right:\n"
            f"   {a} + {b * c} - {d // e} = {a + b * c} - {d // e} = {correct_val}."
        )

    elif variant == "nested_parentheses":
        # a * [b + (c - d) * e]
        e = random.randint(2, 4)
        d = random.randint(1, 5)
        c = d + random.randint(2, 6)
        b = random.randint(3, 8)
        a = random.randint(2, 5)
        # inner = c - d
        # bracket = b + (c - d) * e
        bracket = b + (c - d) * e
        correct_val = a * bracket
        wrong_order = a * ((b + (c - d)) * e)
        correct = str(correct_val)
        distractors = [str(wrong_order), str(correct_val + a), str(correct_val - bracket)]
        trap_map[str(wrong_order)] = "formula_selection_mistake"
        question = f"Evaluate: {a} * [{b} + ({c} - {d}) * {e}]"
        explanation = (
            f"Evaluate from inside out:\n"
            f"1. Innermost parenthesis: ({c} - {d}) = {c - d}\n"
            f"2. Inside square brackets, multiply before adding: ({c - d}) * {e} = {(c - d) * e}\n"
            f"   Then add {b}: {b} + {(c - d) * e} = {bracket}\n"
            f"3. Multiply by {a}: {a} * {bracket} = {correct_val}."
        )

    elif variant == "mult_div_left_right":
        # Classic trap: A / B * C. People mistakenly compute B * C first!
        b = random.choice([2, 3, 4])
        mult = random.randint(3, 8)
        a = b * mult
        c = random.randint(2, 5)
        # a / b * c = (a / b) * c
        correct_val = (a // b) * c
        wrong_denom = a // (b * c) if a % (b * c) == 0 else f"{a}/{b * c}"
        correct = str(correct_val)
        distractors = [str(wrong_denom), str(correct_val + 1), str(correct_val * 2)]
        trap_map[str(wrong_denom)] = "formula_selection_mistake"
        question = f"Evaluate: {a} / {b} * {c}"
        explanation = (
            f"Multiplication and division have EQUAL priority and must be evaluated from LEFT TO RIGHT:\n"
            f"1. First evaluate {a} / {b} = {a // b}\n"
            f"2. Then evaluate ({a // b}) * {c} = {correct_val}.\n"
            f"Common Trap: Multiplying {b} * {c} first violates left-to-right precedence."
        )

    elif variant == "signed_bodmas":
        # Operations with negative integers and powers
        a = random.choice([2, 3, 4])
        b = random.randint(2, 5)
        c = random.randint(5, 12)
        # -a^2 vs (-a)^2
        use_paren = random.choice([True, False])
        if use_paren:
            expr = f"(-{a})^2 - {b} * (-{c})"
            term1 = (-a) ** 2  # positive
            term2 = b * (-c)   # negative
            correct_val = term1 - term2  # positive + positive
            wrong_sign = -(a ** 2) - term2
            correct = str(correct_val)
            distractors = [str(wrong_sign), str(term1 + term2), str(-correct_val)]
            trap_map[str(wrong_sign)] = "sign_mistake"
            question = f"Evaluate: {expr}"
            explanation = (
                f"1. With parentheses, (-{a})^2 = (-{a}) * (-{a}) = +{term1}.\n"
                f"2. Multiplication: {b} * (-{c}) = {term2}.\n"
                f"3. Subtraction: {term1} - ({term2}) = {term1} + {abs(term2)} = {correct_val}."
            )
        else:
            expr = f"-{a}^2 + {b} * (-{c})"
            term1 = -(a ** 2)  # negative because exponent applies to a, not -
            term2 = b * (-c)   # negative
            correct_val = term1 + term2
            wrong_pos = (a ** 2) + term2
            correct = str(correct_val)
            distractors = [str(wrong_pos), str(abs(correct_val)), str(term1 - term2)]
            trap_map[str(wrong_pos)] = "sign_mistake"
            question = f"Evaluate: {expr}"
            explanation = (
                f"Note: -{a}^2 means -( {a}^2 ) = -{a**2} because exponentiation precedes unary negation.\n"
                f"Multiplication: {b} * (-{c}) = {term2}.\n"
                f"Sum: -{a**2} + ({term2}) = {correct_val}."
            )

    else:  # tricky_gmat_expressions
        # Expressions with fractions and order of operations
        # (A - B) / (C + D) vs A - B / C + D
        a = random.randint(12, 24)
        b = random.randint(2, 6)
        c = random.randint(2, 5)
        d = random.randint(1, 4)
        # (a + b * c) / d
        num = a + b * c
        if num % d != 0:
            num = d * random.randint(4, 10)
            a = num - b * c
        correct_val = (a + b * c) // d
        wrong_order = ((a + b) * c) // d
        correct = str(correct_val)
        distractors = [str(wrong_order), str(correct_val + 1), str(correct_val - 2)]
        trap_map[str(wrong_order)] = "formula_selection_mistake"
        question = f"Find the value of: ({a} + {b} * {c}) / {d}"
        explanation = (
            f"1. Evaluate inside parenthesis first according to BODMAS:\n"
            f"   Multiplication precedes addition: {b} * {c} = {b * c}.\n"
            f"   Addition: {a} + {b * c} = {a + b * c}.\n"
            f"2. Division by {d}: {a + b * c} / {d} = {correct_val}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="order_of_operations_gmat",
        subvariant=variant,
    )

