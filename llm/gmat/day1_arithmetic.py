"""Day 1: GMAT Quantitative Practice Engine - Arithmetic Foundations (Patterns 5001-5009)

Covers:
- 5001: Number Classification (Natural, Whole, Integers, Signed ops, Sign determination)
- 5002: Odd & Even Integers (Basic, Operations parity, Algebraic, Elimination, Consecutive)
- 5003: Prime & Composite Numbers (Basic, Sqrt check, Composite props, Prime factorization, Twin primes)
- 5004: Factors & Multiples (List & count, Factor checks, Common factors, Multiples, Relations)
- 5005: Divisibility Rules (2/5/10, 3/9, Missing digit, Combined, Elimination)
- 5006: HCF / GCD (Two numbers, Three numbers, Prime factorization, Equal grouping, Remainder HCF)
- 5007: LCM (Two numbers, Three numbers, Prime factorization, Repeating bells, Traffic intervals)
- 5008: HCF & LCM Relationship (Product formula find LCM, Missing num, Find HCF from prod, Ratio relation, Verification)
- 5009: Order of Operations / BODMAS (Basic, Nested parens, Mult/Div left-right, Signed BODMAS, Tricky GMAT)
"""

import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.gmat.common import (
    clamp_level,
    gcd,
    get_all_divisors,
    get_prime_factors,
    is_prime,
    lcm,
    lcm_list,
    make_mcq,
)


# ==============================================================================
# PATTERN 5001: Number Classification
# ==============================================================================

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


# ==============================================================================
# PATTERN 5002: Odd & Even Integers (Parity)
# ==============================================================================

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


# ==============================================================================
# PATTERN 5003: Prime & Composite Numbers
# ==============================================================================

def generate_prime_composite_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "basic_prime_composite",
        "prime_checking_sqrt",
        "composite_properties",
        "canonical_factorization",
        "twin_primes",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "basic_prime_composite":
        q_type = random.choice(["definition_1", "even_prime", "smallest_odd_prime"])
        if q_type == "definition_1":
            question = "How is the integer 1 classified in number theory?"
            correct = "Neither prime nor composite"
            distractors = ["Prime number", "Composite number", "Even number"]
            trap_map["Prime number"] = "conceptual_mistake"
            trap_map["Composite number"] = "conceptual_mistake"
            explanation = (
                "A prime number has exactly two distinct positive divisors: 1 and itself.\n"
                "A composite number has more than two distinct positive divisors.\n"
                "The number 1 has only one divisor (1 itself). Therefore, 1 is neither prime nor composite."
            )
        elif q_type == "even_prime":
            question = "How many even prime numbers exist?"
            correct = "Exactly 1"
            distractors = ["0", "Infinitely many", "2"]
            trap_map["0"] = "conceptual_mistake"
            trap_map["2"] = "careless_mistake"
            explanation = (
                "The only even prime number is 2.\n"
                "Any other even integer is divisible by 2 and greater than 2, making it composite.\n"
                "Thus, there is exactly 1 even prime number."
            )
        else:
            question = "Which of the following is the smallest composite number?"
            correct = "4"
            distractors = ["1", "2", "3"]
            trap_map["1"] = "conceptual_mistake"
            trap_map["2"] = "conceptual_mistake"
            explanation = (
                "1 is neither prime nor composite. 2 and 3 are prime numbers.\n"
                "4 has divisors {1, 2, 4}, making it the smallest composite number."
            )

    elif variant == "prime_checking_sqrt":
        # Testing if a number N is prime by testing primes up to sqrt(N)
        test_candidates = [
            (91, False, 7, 10),
            (97, True, None, 10),
            (119, False, 7, 11),
            (127, True, None, 12),
            (143, False, 11, 12),
            (149, True, None, 13),
            (221, False, 13, 15),
            (223, True, None, 15),
        ]
        num, is_p, factor, bound = random.choice(test_candidates)
        question = f"To determine whether {num} is a prime number, what is the maximum prime you need to test as a divisor?"
        primes_under_bound = [p for p in [2, 3, 5, 7, 11, 13, 17, 19] if p <= bound]
        correct = str(primes_under_bound[-1])
        distractors = [str(bound + 2), str(num // 2), str(primes_under_bound[-2])]
        trap_map[str(num // 2)] = "formula_selection_mistake"
        explanation = (
            f"To test if n is prime, you only need to check prime divisors up to sqrt(n).\n"
            f"Here, sqrt({num}) ≈ {math.isqrt(num)}.{int(math.sqrt(num)*10)%10}.\n"
            f"The primes <= {math.isqrt(num)} are {primes_under_bound}.\n"
            f"The largest prime to check is {correct}."
        )

    elif variant == "composite_properties":
        # Properties of composite numbers and factor counts
        question = "If n is a composite number, what is the MINIMUM number of positive factors it can have?"
        correct = "3"
        distractors = ["2", "4", "1"]
        trap_map["2"] = "conceptual_mistake"  # 2 is prime
        trap_map["4"] = "conceptual_mistake"
        explanation = (
            "Primes have exactly 2 factors (1 and p).\n"
            "Composite numbers must have more than 2 factors.\n"
            "The square of a prime (e.g. 2^2 = 4, 3^2 = 9) has exactly 3 factors: 1, p, and p^2.\n"
            "Thus, the minimum number of positive factors for a composite number is 3."
        )

    elif variant == "canonical_factorization":
        # Prime factorization canonical form
        if level <= 2:
            base_n = random.choice([72, 84, 108, 120, 180])
        elif level <= 4:
            base_n = random.choice([252, 360, 450, 504, 600])
        else:
            base_n = random.choice([756, 840, 900, 1260, 1800])

        factors = get_prime_factors(base_n)
        correct = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(factors.items()))

        # Distractor 1: wrong exponent
        wrong_p = list(factors.keys())[0]
        wrong_factors1 = dict(factors)
        wrong_factors1[wrong_p] += 1
        d1 = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(wrong_factors1.items()))

        # Distractor 2: missed a prime or composite factor left
        d2 = f"4 * {base_n // 4}" if base_n % 4 == 0 else f"{base_n // 3} * 3"

        # Distractor 3: arithmetic slip
        wrong_factors3 = dict(factors)
        wrong_factors3[list(factors.keys())[-1]] -= 1
        d3 = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(wrong_factors3.items()))

        distractors = [d1, d2, d3]
        trap_map[d2] = "conceptual_mistake"  # left composite factor
        trap_map[d1] = "arithmetic_mistake"
        question = f"What is the canonical prime factorization of {base_n}?"
        explanation = (
            f"Decomposing {base_n} into prime factors:\n"
            + "\n".join([f"- Divide by {p} repeatedly" for p in factors.keys()])
            + f"\nCollecting powers of primes gives: {correct}."
        )

    else:  # twin_primes
        pairs = [(3, 5), (5, 7), (11, 13), (17, 19), (29, 31), (41, 43), (59, 61), (71, 73)]
        target_pair = random.choice(pairs)
        fake_pairs = [(7, 9), (13, 15), (21, 23), (25, 27), (33, 35)]
        correct = f"({target_pair[0]}, {target_pair[1]})"
        distractors = [f"({fp[0]}, {fp[1]})" for fp in random.sample(fake_pairs, 3)]
        for d in distractors:
            trap_map[d] = "conceptual_mistake"
        question = "Which of the following pairs represents twin primes?"
        explanation = (
            "Twin primes are pairs of prime numbers that differ by exactly 2 (p and p + 2 where both are prime).\n"
            f"{correct} are both prime numbers with a difference of 2.\n"
            "In other pairs, at least one of the numbers is composite (e.g., 9, 15, 21, 25, 27 are composite)."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="prime_composite_gmat",
        subvariant=variant,
    )


# ==============================================================================
# PATTERN 5004: Factors & Multiples
# ==============================================================================

def generate_factors_multiples_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "list_count_factors",
        "factor_checks",
        "common_factors",
        "list_multiples",
        "factor_multiple_relations",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "list_count_factors":
        # Total number of factors using prime factorization formula (a+1)(b+1)...
        num_pool = [24, 36, 48, 60, 72, 90, 100, 120, 144, 216]
        n = random.choice(num_pool[:4] if level <= 2 else num_pool)
        divs = get_all_divisors(n)
        correct_count = len(divs)
        correct = str(correct_count)
        distractors = [str(correct_count - 1), str(correct_count + 2), str(correct_count - 2)]
        trap_map[str(correct_count - 1)] = "careless_mistake"  # missed 1 or n
        question = f"How many distinct positive factors does the number {n} have?"
        pf = get_prime_factors(n)
        formula_str = " * ".join(f"({e} + 1)" for e in pf.values())
        explanation = (
            f"Prime factorization of {n} is "
            + " * ".join(f"{p}^{e}" for p, e in pf.items())
            + ".\n"
            f"The total number of factors is found by adding 1 to each exponent and multiplying:\n"
            f"Number of factors = {formula_str} = {correct_count}.\n"
            f"(Divisors: {divs})"
        )

    elif variant == "factor_checks":
        # Check whether a given integer is a factor of another
        base = random.randint(12, 30) * (level)
        divisors = get_all_divisors(base)
        correct_factor = random.choice(divisors[1:-1] if len(divisors) > 2 else divisors)
        non_factors = [x for x in range(2, base) if x not in divisors and base % x != 0]
        chosen_non_factors = random.sample(non_factors, min(3, len(non_factors)))
        correct = str(correct_factor)
        distractors = [str(x) for x in chosen_non_factors]
        for d in distractors:
            trap_map[d] = "arithmetic_mistake"
        question = f"Which of the following numbers is a factor of {base}?"
        explanation = (
            f"A number d is a factor of {base} if {base} is divisible by d with no remainder.\n"
            f"{base} / {correct_factor} = {base // correct_factor}, leaving remainder 0.\n"
            f"The other options do not divide {base} evenly."
        )

    elif variant == "common_factors":
        # Common factors of two numbers
        n1 = 12 * level
        n2 = 18 * level
        cf = [d for d in get_all_divisors(n1) if n2 % d == 0]
        correct = str(len(cf))
        distractors = [str(len(cf) - 1), str(len(cf) + 1), str(len(cf) + 2)]
        trap_map[str(len(cf) - 1)] = "careless_mistake"
        question = f"How many common positive factors do {n1} and {n2} share?"
        g = gcd(n1, n2)
        explanation = (
            f"The common factors of {n1} and {n2} are precisely the factors of their GCD.\n"
            f"GCD({n1}, {n2}) = {g}.\n"
            f"Factors of {g} are {cf}.\n"
            f"Thus, there are {len(cf)} common factors."
        )

    elif variant == "list_multiples":
        # Count multiples in a given range [A, B]
        m = random.choice([4, 6, 7, 8, 9, 11, 12])
        low = random.randint(10, 50)
        high = low + random.randint(50, 150) * level
        # Multiples of m in [low, high]
        first_m = ((low + m - 1) // m) * m
        last_m = (high // m) * m
        if first_m <= last_m:
            count = (last_m - first_m) // m + 1
        else:
            count = 0
        correct = str(count)
        distractors = [str(count + 1), str(max(1, count - 1)), str(count + 2)]
        trap_map[str(count + 1)] = "careless_mistake"  # fencepost error
        trap_map[str(max(1, count - 1))] = "careless_mistake"
        question = f"How many multiples of {m} are there between {low} and {high}, inclusive?"
        explanation = (
            f"First multiple >= {low} is {first_m}.\n"
            f"Last multiple <= {high} is {last_m}.\n"
            f"Count of multiples = ({last_m} - {first_m}) / {m} + 1 = {count}."
        )

    else:  # factor_multiple_relations
        question = "If integer a is a factor of integer b, and b is a factor of integer c, which of the following MUST be true?"
        correct = "a is a factor of c"
        distractors = ["c is a factor of a", "a + b = c", "b / a = c"]
        trap_map["c is a factor of a"] = "conceptual_mistake"
        explanation = (
            "Divisibility is transitive:\n"
            "If a divides b, then b = k1 * a.\n"
            "If b divides c, then c = k2 * b = k2 * (k1 * a) = (k1 * k2) * a.\n"
            "Therefore, a is a factor of c."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="factors_multiples_gmat",
        subvariant=variant,
    )


# ==============================================================================
# PATTERN 5005: Divisibility Rules
# ==============================================================================

def generate_divisibility_rules_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "div_by_2_5_10",
        "div_by_3_9",
        "missing_digit_div",
        "combined_divisibility",
        "elimination_drills",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "div_by_2_5_10":
        # Last digit tests
        divisor = random.choice([2, 5, 10])
        if divisor == 10:
            question = "A positive integer is divisible by 10 if and only if:"
            correct = "Its units digit is 0"
            distractors = ["Its units digit is 5", "The sum of its digits is divisible by 10", "It is even"]
            trap_map["The sum of its digits is divisible by 10"] = "conceptual_mistake"
            explanation = "By the divisibility rule for 10, an integer is divisible by 10 if and only if its units digit is 0."
        elif divisor == 5:
            question = "Which condition guarantees that an integer N is divisible by 5 but NOT by 10?"
            correct = "Units digit is 5"
            distractors = ["Units digit is 0", "Units digit is even", "Sum of digits is 5"]
            trap_map["Units digit is 0"] = "conceptual_mistake"  # divisible by 10
            explanation = (
                "An integer is divisible by 5 if its units digit is 0 or 5.\n"
                "If the units digit is 0, it is also divisible by 10.\n"
                "Therefore, for N to be divisible by 5 but not 10, its units digit must be 5."
            )
        else:
            cand = [1234, 5678, 9102, 3456]
            odd_cands = [1235, 5679, 9101, 3457]
            chosen_odd = random.choice(odd_cands)
            correct = str(chosen_odd)
            distractors = [str(x) for x in random.sample(cand, 3)]
            trap_map[distractors[0]] = "careless_mistake"
            question = "Which of the following numbers is NOT divisible by 2?"
            explanation = (
                f"A number is divisible by 2 if its last digit is even (0, 2, 4, 6, 8).\n"
                f"{chosen_odd} ends in {chosen_odd % 10}, an odd digit, so it is not divisible by 2."
            )

    elif variant == "div_by_3_9":
        # Sum of digits rule
        divisor = random.choice([3, 9])
        base_digits = [random.randint(1, 8) for _ in range(4 if level <= 2 else 6)]
        current_sum = sum(base_digits)
        rem = current_sum % divisor
        add_needed = (divisor - rem) % divisor
        # Construct number
        num_str = "".join(map(str, base_digits)) + str(add_needed)
        actual_num = int(num_str)
        # Create non-divisible numbers
        dist_nums = [actual_num + 1, actual_num + 2, actual_num - 1]
        correct = str(actual_num)
        distractors = [str(d) for d in dist_nums]
        for d in distractors:
            trap_map[d] = "arithmetic_mistake"
        question = f"Which of the following numbers is completely divisible by {divisor}?"
        explanation = (
            f"Rule of {divisor}: A number is divisible by {divisor} if and only if the sum of its digits is divisible by {divisor}.\n"
            f"For {actual_num}, the sum of digits is {sum(int(c) for c in str(actual_num))}, which is divisible by {divisor}.\n"
            f"The digit sums for other options do not divide {divisor} evenly."
        )

    elif variant == "missing_digit_div":
        # e.g., 47x2 is divisible by 9, find digit x
        target_div = random.choice([3, 9, 11])
        if target_div == 9:
            d1, d2, d3 = random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)
            cur_sum = d1 + d2 + d3
            needed = (9 - (cur_sum % 9)) % 9
            question = f"In the 4-digit number {d1}{d2}d{d3}, what single digit 'd' makes the number divisible by 9?"
            correct = str(needed)
            distractors = [str((needed + 2) % 10), str((needed + 3) % 10), str((needed + 5) % 10)]
            trap_map[distractors[0]] = "arithmetic_mistake"
            explanation = (
                f"Sum of known digits = {d1} + {d2} + {d3} = {cur_sum}.\n"
                f"For the number to be divisible by 9, the sum of all digits ({cur_sum} + d) must be a multiple of 9.\n"
                f"The unique digit 0 <= d <= 9 satisfying this is d = {needed}."
            )
        elif target_div == 3:
            d1, d2 = random.randint(1, 9), random.randint(1, 9)
            cur_sum = d1 + d2
            needed = (3 - (cur_sum % 3)) % 3
            question = f"What is the LEAST non-zero single digit 'd' such that the 3-digit number {d1}d{d2} is divisible by 3?"
            val = needed if needed != 0 else 3
            correct = str(val)
            distractors = [str((val + 1) % 10), str((val + 2) % 10), str((val + 4) % 10)]
            trap_map[distractors[0]] = "arithmetic_mistake"
            explanation = (
                f"Sum of known digits = {d1} + {d2} = {cur_sum}.\n"
                f"Sum ({cur_sum} + d) must be divisible by 3.\n"
                f"The least non-zero single digit is {correct}."
            )
        else:
            # Divisible by 11: alternating sum
            # For 3-digit number a d b: (a + b - d) = 0 or 11
            a, b = random.randint(2, 6), random.randint(2, 5)
            d_val = a + b
            if d_val < 10:
                question = f"In the 3-digit number {a}d{b}, what single digit 'd' makes the number divisible by 11?"
                correct = str(d_val)
                distractors = [str(abs(a - b)), str((d_val + 1) % 10), str((d_val - 1) % 10)]
                trap_map[str(abs(a - b))] = "conceptual_mistake"
                explanation = (
                    f"A number is divisible by 11 if the alternating sum of its digits is a multiple of 11.\n"
                    f"({a} + {b}) - d = 0 => d = {a} + {b} = {d_val}."
                )
            else:
                question = "A number is divisible by 11 if and only if:"
                correct = "Difference between sum of alternate digits is a multiple of 11"
                distractors = [
                    "Sum of all digits is a multiple of 11",
                    "Last two digits are divisible by 11",
                    "Units digit is 1",
                ]
                trap_map["Sum of all digits is a multiple of 11"] = "conceptual_mistake"
                explanation = "Divisibility by 11 requires that the difference between the sum of digits at odd places and even places is 0 or a multiple of 11."

    elif variant == "combined_divisibility":
        # Divisible by 6 (2 and 3), 12 (3 and 4), 15 (3 and 5), etc.
        div_rule = random.choice([(6, 2, 3), (12, 3, 4), (15, 3, 5), (18, 2, 9)])
        composite_div, f1, f2 = div_rule
        question = f"For an integer to be divisible by {composite_div}, it must satisfy which two simultaneous conditions?"
        correct = f"Divisible by {f1} and {f2}"
        distractors = [
            f"Divisible by {f1} or {f2}",
            f"Divisible by {f1 + 1} and {f2 - 1}",
            f"Divisible by {composite_div // 2} only",
        ]
        trap_map[f"Divisible by {f1} or {f2}"] = "conceptual_mistake"
        explanation = (
            f"Since {f1} and {f2} are coprime (GCD = 1) and {f1} * {f2} = {composite_div}, "
            f"a number is divisible by {composite_div} if and only if it is simultaneously divisible by BOTH {f1} and {f2}."
        )

    else:  # elimination_drills
        # Which of the following numbers is divisible by both 4 and 9? (i.e. by 36)
        cand36 = random.choice([144, 216, 288, 324, 432, 576])
        wrong1 = cand36 + 2   # ends in even but not div by 4
        wrong2 = cand36 + 4   # div by 4 but not by 9
        wrong3 = cand36 + 9   # div by 9 but not by 4
        correct = str(cand36)
        distractors = [str(wrong1), str(wrong2), str(wrong3)]
        trap_map[str(wrong2)] = "conceptual_mistake"  # checked only one condition
        trap_map[str(wrong3)] = "conceptual_mistake"
        question = "Which of the following numbers is divisible by BOTH 4 and 9?"
        explanation = (
            f"To be divisible by both 4 and 9 (and thus 36):\n"
            f"1. Divisibility by 4: Last 2 digits must be divisible by 4.\n"
            f"2. Divisibility by 9: Sum of digits must be divisible by 9.\n"
            f"Testing {cand36}: Last two digits ({cand36 % 100}) are divisible by 4, "
            f"and digit sum ({sum(int(c) for c in str(cand36))}) is divisible by 9.\n"
            f"None of the other options satisfy both criteria."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="divisibility_rules_gmat",
        subvariant=variant,
    )


# ==============================================================================
# PATTERN 5006: HCF / GCD
# ==============================================================================

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


# ==============================================================================
# PATTERN 5007: LCM (Least Common Multiple)
# ==============================================================================

def generate_lcm_gmat(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "lcm_two_numbers",
        "lcm_three_numbers",
        "prime_factorization_lcm",
        "repeating_events_bells",
        "traffic_intervals",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)
    trap_map: Dict[str, str] = {}

    if variant == "lcm_two_numbers":
        a = random.choice([6, 8, 9, 10, 12, 14, 15, 18]) * (1 if level <= 2 else 2)
        b = random.choice([4, 6, 10, 15, 16, 20, 24]) * (1 if level <= 2 else 2)
        while a == b:
            b += 2
        ans = lcm(a, b)
        correct = str(ans)
        distractors = [str(a * b), str(ans // 2) if (ans // 2) % min(a, b) == 0 else str(ans * 2), str(gcd(a, b))]
        trap_map[str(a * b)] = "formula_selection_mistake"  # product instead of LCM
        trap_map[str(gcd(a, b))] = "conceptual_mistake"  # gave HCF instead of LCM
        question = f"What is the Least Common Multiple (LCM) of {a} and {b}?"
        explanation = (
            f"To find LCM({a}, {b}):\n"
            f"Using formula LCM(a, b) = (a * b) / GCD(a, b):\n"
            f"GCD({a}, {b}) = {gcd(a, b)}.\n"
            f"LCM({a}, {b}) = ({a} * {b}) / {gcd(a, b)} = {ans}."
        )

    elif variant == "lcm_three_numbers":
        nums = random.choice([
            [6, 8, 12],
            [10, 15, 20],
            [12, 18, 24],
            [14, 21, 28],
            [15, 25, 30],
        ])
        if level >= 4:
            nums = [n * 2 for n in nums]
        ans = lcm_list(nums)
        correct = str(ans)
        distractors = [str(ans * 2), str(nums[0] * nums[1] * nums[2]), str(ans // 2)]
        trap_map[str(nums[0] * nums[1] * nums[2])] = "formula_selection_mistake"
        question = f"Calculate the Least Common Multiple (LCM) of the three numbers: {nums[0]}, {nums[1]}, and {nums[2]}."
        explanation = (
            f"Find LCM({nums[0]}, {nums[1]}) = {lcm(nums[0], nums[1])}.\n"
            f"Then find LCM({lcm(nums[0], nums[1])}, {nums[2]}) = {ans}.\n"
            f"Thus, LCM({nums[0]}, {nums[1]}, {nums[2]}) = {ans}."
        )

    elif variant == "prime_factorization_lcm":
        question = (
            "If P = 2^4 * 3^2 * 5 and Q = 2^3 * 3^3 * 7, "
            "what is the Least Common Multiple (LCM) of P and Q?"
        )
        correct = "2^4 * 3^3 * 5 * 7"
        distractors = [
            "2^3 * 3^2",
            "2^4 * 3^3",
            "2^7 * 3^5 * 5 * 7",
        ]
        trap_map["2^3 * 3^2"] = "conceptual_mistake"  # That's HCF!
        trap_map["2^7 * 3^5 * 5 * 7"] = "formula_selection_mistake"  # product
        explanation = (
            "LCM takes the MAXIMUM power of every prime factor appearing in either factorization:\n"
            "- For prime 2: max(4, 3) = 4 -> 2^4\n"
            "- For prime 3: max(2, 3) = 3 -> 3^3\n"
            "- For prime 5: appears in P -> 5^1\n"
            "- For prime 7: appears in Q -> 7^1\n"
            "LCM = 2^4 * 3^3 * 5 * 7."
        )

    elif variant == "repeating_events_bells":
        # Church bells / alarms tolling together
        t1, t2, t3 = random.choice([
            (6, 8, 12),
            (9, 12, 15),
            (10, 15, 25),
            (12, 16, 24),
        ])
        ans_sec = lcm_list([t1, t2, t3])
        correct = f"{ans_sec} seconds"
        distractors = [
            f"{ans_sec * 2} seconds",
            f"{t1 + t2 + t3} seconds",
            f"{ans_sec // 2} seconds",
        ]
        trap_map[f"{t1 + t2 + t3} seconds"] = "conceptual_mistake"
        question = (
            f"Three bells toll at intervals of {t1}, {t2}, and {t3} seconds respectively. "
            f"If they toll together now, after how many seconds will they next toll together?"
        )
        explanation = (
            f"The bells will toll together at a time that is a common multiple of {t1}, {t2}, and {t3}.\n"
            f"The earliest such time is their Least Common Multiple (LCM).\n"
            f"LCM({t1}, {t2}, {t3}) = {ans_sec}.\n"
            f"Thus, they toll together every {ans_sec} seconds."
        )

    else:  # traffic_intervals
        # Traffic lights changing simultaneously
        t1, t2 = random.choice([(45, 60), (30, 45), (40, 60), (48, 72)])
        ans_sec = lcm(t1, t2)
        minutes = ans_sec // 60
        secs = ans_sec % 60
        time_str = f"{minutes} min {secs} sec" if secs != 0 else f"{minutes} minutes"
        correct = time_str
        distractors = [
            f"{minutes + 1} minutes",
            f"{minutes * 2} minutes",
            f"{t1 + t2} seconds",
        ]
        trap_map[f"{t1 + t2} seconds"] = "conceptual_mistake"
        question = (
            f"Traffic lights at two different road crossings change after every {t1} seconds and {t2} seconds respectively. "
            f"If they change simultaneously at 8:00 AM, how long after 8:00 AM will they change together next?"
        )
        explanation = (
            f"The time until they next change simultaneously is LCM({t1}, {t2}) seconds.\n"
            f"LCM({t1}, {t2}) = {ans_sec} seconds.\n"
            f"Converting {ans_sec} seconds: {ans_sec} / 60 = {time_str}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="lcm_gmat",
        subvariant=variant,
    )


# ==============================================================================
# PATTERN 5008: HCF & LCM Relationship (Product Formula)
# ==============================================================================

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


# ==============================================================================
# PATTERN 5009: Order of Operations / BODMAS
# ==============================================================================

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


# ==============================================================================
# REGISTRIES & METADATA
# ==============================================================================

DAY1_GENERATORS = {
    5001: generate_number_classification,
    "number_classification": generate_number_classification,
    5002: generate_odd_even_gmat,
    "odd_even_gmat": generate_odd_even_gmat,
    5003: generate_prime_composite_gmat,
    "prime_composite_gmat": generate_prime_composite_gmat,
    5004: generate_factors_multiples_gmat,
    "factors_multiples_gmat": generate_factors_multiples_gmat,
    5005: generate_divisibility_rules_gmat,
    "divisibility_rules_gmat": generate_divisibility_rules_gmat,
    5006: generate_hcf_gcd_gmat,
    "hcf_gcd_gmat": generate_hcf_gcd_gmat,
    5007: generate_lcm_gmat,
    "lcm_gmat": generate_lcm_gmat,
    5008: generate_hcf_lcm_relation_gmat,
    "hcf_lcm_relation_gmat": generate_hcf_lcm_relation_gmat,
    5009: generate_order_of_operations_gmat,
    "order_of_operations_gmat": generate_order_of_operations_gmat,
}

DAY1_PATTERNS_METADATA = {
    5001: {
        "id": 5001,
        "name": "number_classification",
        "title": "Number Classification",
        "description": "Natural numbers, whole numbers, integers ordering, signed operations, and sign determination.",
        "variants": [
            "natural_numbers",
            "whole_numbers",
            "integers_ordering",
            "signed_operations",
            "sign_determination",
        ],
    },
    5002: {
        "id": 5002,
        "name": "odd_even_gmat",
        "title": "Odd & Even Integers (Parity)",
        "description": "Parity rules, operations, algebraic parity, GMAT parity elimination, and consecutive integers.",
        "variants": [
            "basic_classification",
            "operations_parity",
            "algebraic_parity",
            "gmat_parity_elimination",
            "consecutive_integers",
        ],
    },
    5003: {
        "id": 5003,
        "name": "prime_composite_gmat",
        "title": "Prime & Composite Numbers",
        "description": "Prime identification, square root bound checking, composite properties, canonical factorization, and twin primes.",
        "variants": [
            "basic_prime_composite",
            "prime_checking_sqrt",
            "composite_properties",
            "canonical_factorization",
            "twin_primes",
        ],
    },
    5004: {
        "id": 5004,
        "name": "factors_multiples_gmat",
        "title": "Factors & Multiples",
        "description": "Counting factors via prime powers, factor verification, common factors, listing multiples in ranges, and factor-multiple relations.",
        "variants": [
            "list_count_factors",
            "factor_checks",
            "common_factors",
            "list_multiples",
            "factor_multiple_relations",
        ],
    },
    5005: {
        "id": 5005,
        "name": "divisibility_rules_gmat",
        "title": "Divisibility Rules",
        "description": "Divisibility rules for 2/5/10, 3/9, missing digit deduction, combined divisibility of coprimes, and elimination drills.",
        "variants": [
            "div_by_2_5_10",
            "div_by_3_9",
            "missing_digit_div",
            "combined_divisibility",
            "elimination_drills",
        ],
    },
    5006: {
        "id": 5006,
        "name": "hcf_gcd_gmat",
        "title": "HCF / GCD",
        "description": "Highest Common Factor for two and three numbers, prime factorization powers, equal grouping word problems, and remainder constraints.",
        "variants": [
            "hcf_two_numbers",
            "hcf_three_numbers",
            "prime_factorization_method",
            "equal_grouping_word_problems",
            "remainder_hcf",
        ],
    },
    5007: {
        "id": 5007,
        "name": "lcm_gmat",
        "title": "LCM (Least Common Multiple)",
        "description": "LCM for two and three numbers, prime factorization powers, repeating tolling bells, and traffic signal cycles.",
        "variants": [
            "lcm_two_numbers",
            "lcm_three_numbers",
            "prime_factorization_lcm",
            "repeating_events_bells",
            "traffic_intervals",
        ],
    },
    5008: {
        "id": 5008,
        "name": "hcf_lcm_relation_gmat",
        "title": "HCF & LCM Relationship",
        "description": "Product formula (HCF * LCM = a * b), missing number discovery, HCF from product, ratio relations, and three-number verification.",
        "variants": [
            "product_formula_find_lcm",
            "product_formula_find_missing_num",
            "find_hcf_from_product",
            "ratio_product_relation",
            "verification_drills",
        ],
    },
    5009: {
        "id": 5009,
        "name": "order_of_operations_gmat",
        "title": "Order of Operations / BODMAS",
        "description": "BODMAS fundamentals, nested parentheses/brackets, multiplication/division left-to-right rule, signed arithmetic precedence, and tricky GMAT expressions.",
        "variants": [
            "bodmas_basic",
            "nested_parentheses",
            "mult_div_left_right",
            "signed_bodmas",
            "tricky_gmat_expressions",
        ],
    },
}

# Alias by pattern name as well for easy access
for meta in list(DAY1_PATTERNS_METADATA.values()):
    DAY1_PATTERNS_METADATA[meta["name"]] = meta
