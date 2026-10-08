from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_removing_number_from_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_new_average_one_removed",
        "find_removed_value",
        "student_leaves_group",
        "replacement_in_average",
        "multiple_items_removed",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_new_average_one_removed":
        n = random.randint(6, 10)
        orig_avg = random.randint(30, 60)
        delta = random.choice([1, 2, 3])
        # remove a high number so avg drops by delta
        rem_val = orig_avg + (n - 1) * delta
        new_avg = orig_avg - delta
        question = (
            f"The average of {n} numbers is {orig_avg}. "
            f"If one number equal to {rem_val} is removed, what is the average of the remaining {n - 1} numbers?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg - 1), str(orig_avg), str(new_avg + 2)]
        trap_map = {
            str(new_avg - 1): "arithmetic_mistake",
            str(orig_avg): "conceptual_mistake",
            str(new_avg + 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: Remaining sum after removing {rem_val} = {n * orig_avg} - {rem_val} = {n * orig_avg - rem_val}.\n"
            f"Step 3: New average = ({n * orig_avg - rem_val}) / {n - 1} = {new_avg}."
        )

    elif subvariant == "find_removed_value":
        n = random.randint(5, 11)
        orig_avg = random.randint(25, 55)
        delta = random.choice([2, 3])
        new_avg = orig_avg - delta
        removed_val = orig_avg + (n - 1) * delta
        question = (
            f"The average of {n} observations is {orig_avg}. "
            f"When one observation is removed, the average of the remaining observations decreases to {new_avg}. "
            f"What was the value of the removed observation?"
        )
        correct = str(removed_val)
        wrong_setup = str(orig_avg + n * delta)
        distractors = [wrong_setup, str(removed_val - 4), str(new_avg - delta)]
        trap_map = {
            wrong_setup: "setup_mistake",
            str(removed_val - 4): "arithmetic_mistake",
            str(new_avg - delta): "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total sum of {n} observations = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: Total sum of {n - 1} remaining observations = ({n - 1}) * {new_avg} = {(n - 1) * new_avg}.\n"
            f"Step 3: Removed observation = {n * orig_avg} - {(n - 1) * new_avg} = {removed_val}."
        )

    elif subvariant == "student_leaves_group":
        n = random.randint(8, 15)
        orig_wt = random.randint(50, 70)
        delta = 1
        leaving_wt = orig_wt + (n - 1) * delta
        question = (
            f"The average weight of {n} members of a sports team is {orig_wt} kg. "
            f"When one member leaves the team, the average weight of the remaining members drops by {delta} kg. "
            f"What was the weight of the member who left?"
        )
        correct = f"{leaving_wt} kg"
        wrong_sub = f"{orig_wt - (n - 1) * delta} kg"
        distractors = [wrong_sub, f"{leaving_wt + 2} kg", f"{orig_wt} kg"]
        trap_map = {
            wrong_sub: "sign_mistake",
            f"{leaving_wt + 2} kg": "arithmetic_mistake",
            f"{orig_wt} kg": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Original total weight = {n} * {orig_wt} = {n * orig_wt} kg.\n"
            f"Step 2: Remaining {n - 1} members have average weight {orig_wt - delta} kg.\n"
            f"Step 3: Remaining sum = {n - 1} * {orig_wt - delta} = {(n - 1) * (orig_wt - delta)} kg.\n"
            f"Step 4: Leaver's weight = {n * orig_wt} - {(n - 1) * (orig_wt - delta)} = {leaving_wt} kg."
        )

    elif subvariant == "replacement_in_average":
        n = random.randint(8, 20)
        old_val = random.randint(40, 80)
        delta = random.choice([2, 3, 4])
        new_val = old_val + n * delta
        question = (
            f"In a group of {n} individuals, a person weighing {old_val} kg is replaced by a new person. "
            f"As a result, the average weight of the group increases by {delta} kg. "
            f"What is the weight of the new person?"
        )
        correct = f"{new_val} kg"
        wrong_no_n = f"{old_val + delta} kg"
        distractors = [wrong_no_n, f"{old_val - n * delta} kg", f"{new_val + delta} kg"]
        trap_map = {
            wrong_no_n: "setup_mistake",
            f"{old_val - n * delta} kg": "sign_mistake",
            f"{new_val + delta} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Net increase in the total weight of the group = {n} members * {delta} kg = {n * delta} kg.\n"
            f"Step 2: Weight of new person = Weight of replaced person + Net Increase.\n"
            f"Step 3: New weight = {old_val} + {n * delta} = {new_val} kg."
        )

    else:  # multiple_items_removed
        n = 8
        orig_avg = 40
        rem_count = 2
        rem_avg = 55
        tot_orig = n * orig_avg  # 320
        tot_rem = rem_count * rem_avg  # 110
        rem_items = n - rem_count  # 6
        new_avg = (tot_orig - tot_rem) // rem_items  # 210 / 6 = 35
        question = (
            f"The average score of {n} students on an exam is {orig_avg}. "
            f"If {rem_count} students with an average score of {rem_avg} leave the class, "
            f"what is the average score of the remaining {rem_items} students?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg - 2), str((orig_avg + rem_avg) // 2), str(new_avg + 3)]
        trap_map = {
            str(new_avg - 2): "arithmetic_mistake",
            str((orig_avg + rem_avg) // 2): "average_weighted_mistake",
            str(new_avg + 3): "setup_mistake",
        }
        explanation = (
            f"Step 1: Original total score = {n} * {orig_avg} = {tot_orig}.\n"
            f"Step 2: Total score of leaving students = {rem_count} * {rem_avg} = {tot_rem}.\n"
            f"Step 3: Remaining total score = {tot_orig} - {tot_rem} = {tot_orig - tot_rem}.\n"
            f"Step 4: Remaining average = {tot_orig - tot_rem} / {rem_items} = {new_avg}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="removing_number_from_average",
        subvariant=subvariant,
    )

