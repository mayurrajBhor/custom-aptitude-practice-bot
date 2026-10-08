from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_average_basics(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "compute_average",
        "find_sum_from_average",
        "find_count_from_sum_and_avg",
        "average_of_consecutive_integers",
        "average_of_multiples",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "compute_average":
        n = random.randint(4, 6) if level <= 3 else random.randint(5, 7)
        avg = random.randint(15, 45)
        # Generate n numbers that average to avg
        diffs = [random.randint(-10, 10) for _ in range(n - 1)]
        diffs.append(-sum(diffs))
        nums = [avg + d for d in diffs]
        nums_str = ", ".join(map(str, nums))
        question = f"What is the arithmetic mean (average) of the following numbers: {nums_str}?"
        correct = str(avg)
        distractors = [str(avg + 2), str(avg - 2), str(sum(nums) // (n - 1))]
        trap_map = {
            str(avg + 2): "arithmetic_mistake",
            str(avg - 2): "arithmetic_mistake",
            str(sum(nums) // (n - 1)): "setup_mistake",
        }
        explanation = (
            f"Step 1: Sum the {n} numbers: {sum(nums)}.\n"
            f"Step 2: Divide the sum by the count of numbers ({n}): {sum(nums)} / {n} = {avg}."
        )

    elif subvariant == "find_sum_from_average":
        n = random.randint(5, 12)
        avg = random.randint(20, 60)
        tot = n * avg
        question = (
            f"A group of {n} students took a test, scoring an average of {avg} points. "
            f"What was the total sum of all their test scores?"
        )
        correct = str(tot)
        distractors = [str(tot + avg), str(tot - avg), str(int(tot / n))]
        trap_map = {
            str(tot + avg): "setup_mistake",
            str(tot - avg): "setup_mistake",
            str(int(tot / n)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the fundamental formula: Sum = Average * Count.\n"
            f"Step 2: Sum = {avg} * {n} = {tot}."
        )

    elif subvariant == "find_count_from_sum_and_avg":
        n = random.randint(6, 15)
        avg = random.randint(14, 35)
        tot = n * avg
        question = (
            f"A set of measurements has a total sum of {tot} and an average value of {avg}. "
            f"How many measurements are in the set?"
        )
        correct = str(n)
        distractors = [str(n + 1), str(n - 1), str(tot * avg)]
        trap_map = {
            str(n + 1): "arithmetic_mistake",
            str(n - 1): "arithmetic_mistake",
            str(tot * avg): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the relationship: Count = Sum / Average.\n"
            f"Step 2: Count = {tot} / {avg} = {n}."
        )

    elif subvariant == "average_of_consecutive_integers":
        start = random.randint(11, 40)
        k = random.choice([7, 9, 11, 15])  # odd number of integers
        end = start + k - 1
        avg = (start + end) // 2
        question = f"What is the average of all consecutive integers from {start} to {end}, inclusive?"
        correct = str(avg)
        distractors = [str(avg + 1), str(avg - 1), str(end - start)]
        trap_map = {
            str(avg + 1): "arithmetic_mistake",
            str(avg - 1): "arithmetic_mistake",
            str(end - start): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: For any evenly spaced sequence, Average = (First Term + Last Term) / 2.\n"
            f"Step 2: Average = ({start} + {end}) / 2 = {start + end} / 2 = {avg}."
        )

    else:  # average_of_multiples
        m = random.choice([3, 4, 5, 6, 7, 8])
        k = random.choice([7, 9, 11, 13])  # odd number of multiples
        avg = (m * (k + 1)) // 2
        question = f"What is the average of the first {k} positive multiples of {m}?"
        correct = str(avg)
        distractors = [str(avg + m), str(avg - m), str(m * k)]
        trap_map = {
            str(avg + m): "arithmetic_mistake",
            str(avg - m): "arithmetic_mistake",
            str(m * k): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: The first multiple is {m}*1 = {m}, and the {k}th multiple is {m}*{k} = {m * k}.\n"
            f"Step 2: Since multiples form an arithmetic progression, Average = (First + Last) / 2.\n"
            f"Step 3: Average = ({m} + {m * k}) / 2 = {m + m * k} / 2 = {avg}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="average_basics",
        subvariant=subvariant,
    )

