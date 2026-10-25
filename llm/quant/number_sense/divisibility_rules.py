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

