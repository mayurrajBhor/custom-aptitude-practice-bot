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

