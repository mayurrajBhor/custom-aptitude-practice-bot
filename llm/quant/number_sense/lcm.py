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

