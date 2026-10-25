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

