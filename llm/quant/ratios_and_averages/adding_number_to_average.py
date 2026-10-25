from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_adding_number_to_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "find_new_average_one_added",
        "find_added_value",
        "teacher_joins_class",
        "batsman_or_player_score",
        "multiple_items_added",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "find_new_average_one_added":
        n = random.randint(4, 9)
        orig_avg = random.randint(20, 50)
        # Added value chosen so that (n * orig_avg + val) % (n + 1) == 0
        delta = random.choice([2, 3, 4])
        val = orig_avg + delta * (n + 1)
        new_avg = orig_avg + delta
        question = (
            f"The average of {n} numbers is {orig_avg}. "
            f"If a new number equal to {val} is added to the set, what is the new average of all {n + 1} numbers?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg + 1), str(orig_avg), str((orig_avg + val) // 2)]
        trap_map = {
            str(new_avg + 1): "arithmetic_mistake",
            str(orig_avg): "conceptual_mistake",
            str((orig_avg + val) // 2): "average_weighted_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: New total sum with {val} added = {n * orig_avg} + {val} = {n * orig_avg + val}.\n"
            f"Step 3: New average = {n * orig_avg + val} / {n + 1} = {new_avg}."
        )

    elif subvariant == "find_added_value":
        n = random.randint(5, 12)
        orig_avg = random.randint(30, 70)
        delta = random.choice([1, 2, 3])
        new_avg = orig_avg + delta
        added_val = orig_avg + (n + 1) * delta
        question = (
            f"A group of {n} test scores had an average of {orig_avg}. "
            f"After adding one more test score, the average score increased to {new_avg}. "
            f"What was the value of the added test score?"
        )
        correct = str(added_val)
        wrong_unweighted = str(orig_avg + n * delta)
        distractors = [wrong_unweighted, str(new_avg + delta), str(added_val + 5)]
        trap_map = {
            wrong_unweighted: "setup_mistake",
            str(new_avg + delta): "average_weighted_mistake",
            str(added_val + 5): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Original total sum = {n} * {orig_avg} = {n * orig_avg}.\n"
            f"Step 2: New total sum with {n + 1} scores = {n + 1} * {new_avg} = {(n + 1) * new_avg}.\n"
            f"Step 3: Added score = {(n + 1) * new_avg} - {n * orig_avg} = {added_val}."
        )

    elif subvariant == "teacher_joins_class":
        n_students = random.randint(14, 24)
        avg_age = random.choice([12, 13, 14, 15])
        delta = random.choice([1, 2])
        teacher_age = avg_age + (n_students + 1) * delta
        question = (
            f"In a classroom of {n_students} students, the average age is {avg_age} years. "
            f"When the teacher joins the class, the average age increases by {delta} year"
            + ("s" if delta > 1 else "")
            + ". How old is the teacher?"
        )
        correct = f"{teacher_age} years"
        wrong_setup = f"{avg_age + n_students * delta} years"
        distractors = [wrong_setup, f"{teacher_age - 3} years", f"{avg_age + delta} years"]
        trap_map = {
            wrong_setup: "setup_mistake",
            f"{teacher_age - 3} years": "arithmetic_mistake",
            f"{avg_age + delta} years": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Total age of {n_students} students = {n_students} * {avg_age} = {n_students * avg_age}.\n"
            f"Step 2: Total members now = {n_students + 1}, with new average age = {avg_age + delta}.\n"
            f"Step 3: Total age of group = {n_students + 1} * {avg_age + delta} = {(n_students + 1) * (avg_age + delta)}.\n"
            f"Step 4: Teacher's age = {(n_students + 1) * (avg_age + delta)} - {n_students * avg_age} = {teacher_age} years."
        )

    elif subvariant == "batsman_or_player_score":
        innings = random.choice([8, 10, 12])
        avg = random.randint(35, 55)
        new_innings = innings + 1
        delta = random.choice([2, 3, 4])
        score = avg + new_innings * delta
        new_avg = avg + delta
        question = (
            f"A cricketer has an average of {avg} runs in {innings} innings. "
            f"In his next inning, he scores {score} runs. What is his new batting average?"
        )
        correct = str(new_avg)
        distractors = [str(new_avg + 1), str((avg + score) // 2), str(avg + delta + 2)]
        trap_map = {
            str(new_avg + 1): "arithmetic_mistake",
            str((avg + score) // 2): "average_weighted_mistake",
            str(avg + delta + 2): "setup_mistake",
        }
        explanation = (
            f"Step 1: Runs scored in first {innings} innings = {innings} * {avg} = {innings * avg}.\n"
            f"Step 2: Total runs after {new_innings} innings = {innings * avg} + {score} = {innings * avg + score}.\n"
            f"Step 3: New average = {innings * avg + score} / {new_innings} = {new_avg} runs."
        )

    else:  # multiple_items_added
        n1 = 4
        a1 = random.randint(20, 30)
        n2 = 2
        a2 = random.randint(35, 45)
        combined_tot = n1 * a1 + n2 * a2
        combined_avg = combined_tot // (n1 + n2)
        # adjust a2 to make clean integer division
        rem = combined_tot % (n1 + n2)
        if rem != 0:
            a2 += (n1 + n2 - rem) // n2
            combined_tot = n1 * a1 + n2 * a2
            combined_avg = combined_tot // (n1 + n2)
        question = (
            f"A group of {n1} items has an average weight of {a1} kg. "
            f"Another {n2} items with an average weight of {a2} kg are added to the group. "
            f"What is the average weight of the combined {n1 + n2} items?"
        )
        correct = f"{combined_avg} kg"
        simple_mean = f"{(a1 + a2) // 2} kg"
        distractors = [simple_mean, f"{combined_avg + 2} kg", f"{combined_avg - 2} kg"]
        trap_map = {
            simple_mean: "average_weighted_mistake",
            f"{combined_avg + 2} kg": "arithmetic_mistake",
            f"{combined_avg - 2} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total weight of first group = {n1} * {a1} = {n1 * a1} kg.\n"
            f"Step 2: Total weight of second group = {n2} * {a2} = {n2 * a2} kg.\n"
            f"Step 3: Combined total weight = {n1 * a1} + {n2 * a2} = {combined_tot} kg.\n"
            f"Step 4: Combined average = {combined_tot} / ({n1} + {n2}) = {combined_avg} kg."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="adding_number_to_average",
        subvariant=subvariant,
    )

