from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_average_change_shortcut(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_added_via_deviation",
        "find_removed_via_deviation",
        "find_replacement_diff",
        "find_count_via_deviation",
        "sum_of_deviations_zero",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_added_via_deviation":
        # Deviation shortcut: Added = Old_Avg + (N+1)*Delta
        n = random.randint(10, 25)
        old_avg = random.randint(40, 80)
        delta = random.choice([2, 3])
        added_val = old_avg + (n + 1) * delta
        question = (
            f"A group of {n} employees has an average monthly bonus of ${old_avg}. "
            f"When a new employee joins, the average bonus of the group increases by ${delta}. "
            f"Using the deviation shortcut (New Value = Old Average + (N + 1) * Delta), "
            f"what is the bonus received by the new employee?"
        )
        correct = f"${added_val}"
        wrong_n = f"${old_avg + n * delta}"
        distractors = [wrong_n, f"${added_val + 5}", f"${old_avg + delta}"]
        trap_map = {
            wrong_n: "setup_mistake",
            f"${added_val + 5}": "arithmetic_mistake",
            f"${old_avg + delta}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: The new member must provide the previous average plus ${delta} for each member of the new group.\n"
            f"Step 2: Total members in new group = {n} + 1 = {n + 1}.\n"
            f"Step 3: Added bonus = Old Average + ({n + 1} * Delta) = ${old_avg} + ({n + 1} * ${delta}) = ${added_val}."
        )

    elif subvariant == "find_removed_via_deviation":
        # Deviation shortcut: Removed = Old_Avg + (N-1)*Delta (when average drops by delta)
        n = random.randint(12, 24)
        old_avg = random.randint(50, 80)
        delta = random.choice([1, 2])
        removed_val = old_avg + (n - 1) * delta
        question = (
            f"A cohort of {n} trainees had an average assessment score of {old_avg}. "
            f"When one trainee's score was removed, the average score of the remaining group dropped by {delta} point"
            + ("s" if delta > 1 else "")
            + ". What was the score of the removed trainee?"
        )
        correct = str(removed_val)
        wrong_sub = str(old_avg - (n - 1) * delta)
        distractors = [wrong_sub, str(old_avg + n * delta), str(removed_val + 2)]
        trap_map = {
            wrong_sub: "sign_mistake",
            str(old_avg + n * delta): "setup_mistake",
            str(removed_val + 2): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Because removing this score reduced the average for the remaining {n - 1} trainees by {delta},\n"
            f"the removed score contributed a total surplus of ({n - 1}) * {delta} above the mean.\n"
            f"Step 2: Removed score = {old_avg} + ({n - 1}) * {delta} = {removed_val}."
        )

    elif subvariant == "find_replacement_diff":
        n = random.randint(10, 30)
        delta = random.choice([1.5, 2.0, 2.5, 3.0])
        diff = int(round(n * delta))
        question = (
            f"In a team of {n} researchers, one person is replaced by a new recruit. "
            f"If the average age of the team decreases by {delta} years, "
            f"by how many years is the new recruit younger than the replaced researcher?"
        )
        correct = f"{diff} years"
        distractors = [f"{int(delta)} years", f"{diff + int(delta)} years", f"{int(round((n - 1) * delta))} years"]
        trap_map = {
            f"{int(delta)} years": "setup_mistake",
            f"{diff + int(delta)} years": "arithmetic_mistake",
            f"{int(round((n - 1) * delta))} years": "setup_mistake",
        }
        explanation = (
            f"Step 1: The total reduction across all {n} members is N * Delta.\n"
            f"Step 2: Age difference = {n} * {delta} = {diff} years."
        )

    elif subvariant == "find_count_via_deviation":
        # n = (X - B) / (B - A)
        old_avg = 50
        new_avg = 55
        added_val = 90
        # n = (90 - 55) / (55 - 50) = 35 / 5 = 7
        n = (added_val - new_avg) // (new_avg - old_avg)
        question = (
            f"A group of friends had an average test score of {old_avg}. "
            f"When an additional friend scoring {added_val} joined the group, "
            f"the average score rose to {new_avg}. "
            f"How many friends were originally in the group?"
        )
        correct = str(n)
        distractors = [str(n + 1), str(max(1, n - 1)), str((added_val - old_avg) // (new_avg - old_avg))]
        trap_map = {
            str(n + 1): "setup_mistake",
            str(max(1, n - 1)): "arithmetic_mistake",
            str((added_val - old_avg) // (new_avg - old_avg)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Use the deviation balance method: Initial Count n = (Added Value - New Average) / (New Average - Old Average).\n"
            f"Step 2: Surplus provided to existing members = {added_val} - {new_avg} = {added_val - new_avg}.\n"
            f"Step 3: Increase received per existing member = {new_avg} - {old_avg} = {new_avg - old_avg}.\n"
            f"Step 4: Initial Count = {added_val - new_avg} / {new_avg - old_avg} = {n} friends."
        )

    else:  # sum_of_deviations_zero
        # Deviations from mean always sum to 0
        devs = [-5, 8, -3, 2]
        last_dev = -sum(devs)
        devs_str = ", ".join([f"{'+' if d > 0 else ''}{d}" for d in devs])
        question = (
            f"For a set of 5 numbers, the deviations of the first 4 numbers from their arithmetic mean are "
            f"{devs_str}. What is the deviation of the fifth number from the mean?"
        )
        correct = f"{'+' if last_dev > 0 else ''}{last_dev}"
        wrong_sign = f"{'+' if -last_dev > 0 else ''}{-last_dev}"
        distractors = [wrong_sign, "0", "+1"]
        trap_map = {
            wrong_sign: "sign_mistake",
            "0": "conceptual_mistake",
            "+1": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: By mathematical definition, the sum of all deviations from the arithmetic mean is always zero: Sum(d_i) = 0.\n"
            f"Step 2: Sum of known deviations = {sum(devs)}.\n"
            f"Step 3: Deviation of the 5th number = -({sum(devs)}) = {correct}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="average_change_shortcut",
        subvariant=subvariant,
    )

