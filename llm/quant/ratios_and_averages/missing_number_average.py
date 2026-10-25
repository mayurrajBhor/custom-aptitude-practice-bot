from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_missing_number_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "one_missing_in_set",
        "test_score_target",
        "consecutive_series_with_unknown",
        "two_missing_with_relation",
        "missing_sales_or_daily_target",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "one_missing_in_set":
        n = random.randint(4, 6)
        target_avg = random.randint(20, 50)
        total_sum = n * target_avg
        known_nums = [random.randint(target_avg - 15, target_avg + 15) for _ in range(n - 1)]
        missing = total_sum - sum(known_nums)
        nums_str = ", ".join(map(str, known_nums))
        question = (
            f"The average of a set of {n} numbers is {target_avg}. "
            f"If {n - 1} of the numbers are {nums_str}, what is the missing number?"
        )
        correct = str(missing)
        distractors = [str(missing + 2), str(missing - 2), str(target_avg)]
        trap_map = {
            str(missing + 2): "arithmetic_mistake",
            str(missing - 2): "arithmetic_mistake",
            str(target_avg): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total sum of all {n} numbers = {n} * {target_avg} = {total_sum}.\n"
            f"Step 2: Sum of known numbers = {sum(known_nums)}.\n"
            f"Step 3: Missing number = {total_sum} - {sum(known_nums)} = {missing}."
        )

    elif subvariant == "test_score_target":
        target = random.choice([80, 82, 85, 88, 90])
        # 4 test scores given, find 5th test score
        scores = [random.randint(target - 12, target + 8) for _ in range(4)]
        needed = 5 * target - sum(scores)
        scores_str = ", ".join(map(str, scores))
        question = (
            f"A student scores {scores_str} on four history tests. "
            f"What score must the student achieve on the fifth test to attain an overall average of {target}?"
        )
        correct = str(needed)
        distractors = [str(needed + 4), str(needed - 4), str(target)]
        trap_map = {
            str(needed + 4): "arithmetic_mistake",
            str(needed - 4): "arithmetic_mistake",
            str(target): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total points required across 5 tests = 5 * {target} = {5 * target}.\n"
            f"Step 2: Sum of first 4 scores = {sum(scores)}.\n"
            f"Step 3: Required 5th score = {5 * target} - {sum(scores)} = {needed}."
        )

    elif subvariant == "consecutive_series_with_unknown":
        k = random.choice([5, 7])
        avg = random.randint(25, 60)
        largest = avg + (k - 1) // 2
        smallest = avg - (k - 1) // 2
        ask_largest = random.choice([True, False])
        ans = largest if ask_largest else smallest
        term_type = "largest" if ask_largest else "smallest"
        question = (
            f"The average of {k} consecutive integers is {avg}. "
            f"What is the {term_type} of these integers?"
        )
        correct = str(ans)
        other = smallest if ask_largest else largest
        distractors = [str(other), str(avg), str(ans + 1)]
        trap_map = {
            str(other): "careless_mistake",
            str(avg): "setup_mistake",
            str(ans + 1): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: For {k} consecutive integers, the average is the exact middle integer = {avg}.\n"
            f"Step 2: The integers extend {(k - 1) // 2} steps to the left and to the right.\n"
            f"Step 3: The {term_type} integer is {avg} {'+' if ask_largest else '-'} {(k - 1) // 2} = {ans}."
        )

    elif subvariant == "two_missing_with_relation":
        n = 5
        avg = random.randint(30, 60)
        tot = n * avg
        known3 = [avg - 6, avg + 2, avg - 4]
        sum_known = sum(known3)
        rem_sum = tot - sum_known
        d = random.choice([4, 6, 8])
        larger = (rem_sum + d) // 2
        smaller = larger - d
        question = (
            f"The average of 5 numbers is {avg}. Three of the numbers are {known3[0]}, {known3[1]}, and {known3[2]}. "
            f"The remaining two numbers differ by {d}. What is the value of the larger of the two missing numbers?"
        )
        correct = str(larger)
        distractors = [str(smaller), str(rem_sum // 2), str(larger + d)]
        trap_map = {
            str(smaller): "careless_mistake",
            str(rem_sum // 2): "setup_mistake",
            str(larger + d): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total sum = 5 * {avg} = {tot}.\n"
            f"Step 2: Sum of known 3 numbers = {sum_known}.\n"
            f"Step 3: Sum of two missing numbers = {tot} - {sum_known} = {rem_sum}.\n"
            f"Step 4: If smaller is x, larger is x + {d}. 2x + {d} = {rem_sum} => x = {smaller}.\n"
            f"Step 5: The larger missing number is {smaller} + {d} = {larger}."
        )

    else:  # missing_sales_or_daily_target
        days = 6
        target_avg = random.choice([250, 300, 400])
        tot_target = days * target_avg
        sales = [random.randint(target_avg - 50, target_avg + 40) for _ in range(days - 1)]
        needed = tot_target - sum(sales)
        sales_str = ", ".join([f"${s}" for s in sales])
        question = (
            f"A retail shop targets an average daily revenue of ${target_avg} over a 6-day work week. "
            f"If revenues for Monday through Friday were {sales_str}, what must the revenue be on Saturday to reach the target?"
        )
        correct = f"${needed}"
        distractors = [f"${needed + 25}", f"${needed - 25}", f"${target_avg}"]
        trap_map = {
            f"${needed + 25}": "arithmetic_mistake",
            f"${needed - 25}": "arithmetic_mistake",
            f"${target_avg}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total 6-day target revenue = 6 * ${target_avg} = ${tot_target}.\n"
            f"Step 2: Sum of revenues from Monday to Friday = ${sum(sales)}.\n"
            f"Step 3: Saturday revenue needed = ${tot_target} - ${sum(sales)} = ${needed}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="missing_number_average",
        subvariant=subvariant,
    )

