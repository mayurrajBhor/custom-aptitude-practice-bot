from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_weighted_average(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_groups_find_combined",
        "find_ratio_of_counts",
        "three_groups_find_combined",
        "find_missing_group_average",
        "weighted_percentage_marks",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "two_groups_find_combined":
        # n1 * a1 + n2 * a2
        n1, a1, n2, a2 = random.choice([
            (20, 70, 30, 80),  # (1400 + 2400)/50 = 76
            (10, 60, 40, 75),  # (600 + 3000)/50 = 72
            (15, 80, 25, 60),  # (1200 + 1500)/40 = 67.5 -> let's make integer
            (12, 70, 18, 85),  # (840 + 1530)/30 = 2370/30 = 79
            (25, 64, 75, 80),  # (1600 + 6000)/100 = 76
        ])
        comb = (n1 * a1 + n2 * a2) // (n1 + n2)
        question = (
            f"Section A has {n1} students with an average score of {a1}. "
            f"Section B has {n2} students with an average score of {a2}. "
            f"What is the combined average score of all students in both sections?"
        )
        correct = str(comb)
        unweighted = str((a1 + a2) // 2)
        distractors = [unweighted, str(comb + 2), str(comb - 2)]
        trap_map = {
            unweighted: "average_weighted_mistake",
            str(comb + 2): "arithmetic_mistake",
            str(comb - 2): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Sum for Section A = {n1} * {a1} = {n1 * a1}.\n"
            f"Step 2: Sum for Section B = {n2} * {a2} = {n2 * a2}.\n"
            f"Step 3: Total sum = {n1 * a1} + {n2 * a2} = {n1 * a1 + n2 * a2}.\n"
            f"Step 4: Total students = {n1} + {n2} = {n1 + n2}.\n"
            f"Step 5: Combined Average = {n1 * a1 + n2 * a2} / {n1 + n2} = {comb}."
        )

    elif subvariant == "find_ratio_of_counts":
        # Alligation: n1/n2 = (a2 - a_avg) / (a_avg - a1)
        a1, a2 = 60, 90
        # choose a_avg = 72 => (90 - 72) : (72 - 60) = 18 : 12 = 3 : 2
        a_avg = 72
        d1 = a2 - a_avg  # 18
        d2 = a_avg - a1  # 12
        g = gcd(d1, d2)
        r1, r2 = d1 // g, d2 // g
        question = (
            f"In a company, junior developers have an average hourly rate of ${a1} and senior developers have an average hourly rate of ${a2}. "
            f"If the company-wide average hourly rate for developers is ${a_avg}, what is the ratio of junior developers to senior developers?"
        )
        correct = f"{r1}:{r2}"
        distractors = [f"{r2}:{r1}", "1:1", f"{a1 // 10}:{a2 // 10}"]
        trap_map = {
            f"{r2}:{r1}": "ratio_interpretation_mistake",
            "1:1": "average_weighted_mistake",
            f"{a1 // 10}:{a2 // 10}": "conceptual_mistake",
        }
        explanation = (
            f"Step 1: Apply the alligation / weighted average ratio rule:\n"
            f"   (Junior Count) / (Senior Count) = |Senior Avg - Overall Avg| / |Overall Avg - Junior Avg|.\n"
            f"Step 2: Distance from Senior Avg = {a2} - {a_avg} = {d1}.\n"
            f"Step 3: Distance from Junior Avg = {a_avg} - {a1} = {d2}.\n"
            f"Step 4: Ratio = {d1}:{d2} = {r1}:{r2} in simplest terms."
        )

    elif subvariant == "three_groups_find_combined":
        n1, a1 = 10, 60
        n2, a2 = 20, 75
        n3, a3 = 30, 90
        tot_pts = n1 * a1 + n2 * a2 + n3 * a3  # 600 + 1500 + 2700 = 4800
        tot_n = n1 + n2 + n3  # 60
        comb = tot_pts // tot_n  # 80
        question = (
            f"Three training batches of sizes {n1}, {n2}, and {n3} scored averages of {a1}, {a2}, and {a3} respectively. "
            f"What is the overall average score across all three batches?"
        )
        correct = str(comb)
        unweighted = str((a1 + a2 + a3) // 3)
        distractors = [unweighted, str(comb + 3), str(comb - 3)]
        trap_map = {
            unweighted: "average_weighted_mistake",
            str(comb + 3): "arithmetic_mistake",
            str(comb - 3): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total points = ({n1} * {a1}) + ({n2} * {a2}) + ({n3} * {a3}) = {n1 * a1} + {n2 * a2} + {n3 * a3} = {tot_pts}.\n"
            f"Step 2: Total participants = {n1} + {n2} + {n3} = {tot_n}.\n"
            f"Step 3: Combined Average = {tot_pts} / {tot_n} = {comb}."
        )

    elif subvariant == "find_missing_group_average":
        tot_n = 50
        n1 = 20
        n2 = 30
        comb_avg = 74
        a1 = 65
        # 50 * 74 - 20 * 65 = 3700 - 1300 = 2400. 2400 / 30 = 80
        a2 = (tot_n * comb_avg - n1 * a1) // n2
        question = (
            f"A cohort of {tot_n} students has an overall average score of {comb_avg}. "
            f"If {n1} of the students scored an average of {a1}, "
            f"what was the average score of the remaining {n2} students?"
        )
        correct = str(a2)
        distractors = [str(comb_avg), str(a2 + 4), str(a2 - 4)]
        trap_map = {
            str(comb_avg): "conceptual_mistake",
            str(a2 + 4): "arithmetic_mistake",
            str(a2 - 4): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total score for all {tot_n} students = {tot_n} * {comb_avg} = {tot_n * comb_avg}.\n"
            f"Step 2: Total score for first {n1} students = {n1} * {a1} = {n1 * a1}.\n"
            f"Step 3: Total score for remaining {n2} students = {tot_n * comb_avg} - {n1 * a1} = {tot_n * comb_avg - n1 * a1}.\n"
            f"Step 4: Average for remaining students = {tot_n * comb_avg - n1 * a1} / {n2} = {a2}."
        )

    else:  # weighted_percentage_marks
        w1, w2, w3 = 20, 30, 50
        s1, s2, s3 = 90, 80, 70
        tot = (w1 * s1 + w2 * s2 + w3 * s3) // 100  # 1800 + 2400 + 3500 = 7700 // 100 = 77
        question = (
            f"A course grade is calculated with weights: Homework {w1}%, Midterm Exam {w2}%, and Final Exam {w3}%. "
            f"If a student scores {s1}% on Homework, {s2}% on the Midterm, and {s3}% on the Final Exam, "
            f"what is the student's overall weighted course grade?"
        )
        correct = f"{tot}%"
        simple = f"{(s1 + s2 + s3) // 3}%"
        distractors = [simple, f"{tot + 3}%", f"{tot - 3}%"]
        trap_map = {
            simple: "average_weighted_mistake",
            f"{tot + 3}%": "arithmetic_mistake",
            f"{tot - 3}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Compute weighted components:\n"
            f"   Homework: {w1}% * {s1} = {w1 * s1 / 100:.1f}\n"
            f"   Midterm: {w2}% * {s2} = {w2 * s2 / 100:.1f}\n"
            f"   Final Exam: {w3}% * {s3} = {w3 * s3 / 100:.1f}\n"
            f"Step 2: Add weighted scores: {tot}%."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="weighted_average",
        subvariant=subvariant,
    )

