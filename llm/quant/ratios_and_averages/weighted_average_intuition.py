from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_weighted_average_intuition(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "pulled_towards_larger_group",
        "equal_sizes_vs_unequal",
        "teeter_totter_leverage",
        "quick_elimination_bounds",
        "weighted_average_ds_style",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "pulled_towards_larger_group":
        # Group A: 80 people, avg 70. Group B: 20 people, avg 90. Midpoint 80.
        # Combined avg = (5600 + 1800)/100 = 74.
        question = (
            "Class A has 80 students with an average exam score of 70. "
            "Class B has 20 students with an average exam score of 90. "
            "Without calculating the exact number, the combined average score of both classes must be:"
        )
        correct = "Between 70 and 80 (closer to 70)"
        distractors = [
            "Exactly 80 (the simple arithmetic midpoint)",
            "Between 80 and 90 (closer to 90)",
            "Greater than 90",
        ]
        trap_map = {
            "Exactly 80 (the simple arithmetic midpoint)": "average_weighted_mistake",
            "Between 80 and 90 (closer to 90)": "conceptual_mistake",
            "Greater than 90": "conceptual_mistake",
        }
        explanation = (
            "Step 1: The midpoint of 70 and 90 is (70 + 90) / 2 = 80.\n"
            "Step 2: A weighted average is always pulled toward the group with larger weight.\n"
            "Step 3: Since Class A has 80 students and Class B has only 20, the combined average must be strictly closer to 70 than to 90, meaning it lies between 70 and 80."
        )

    elif subvariant == "equal_sizes_vs_unequal":
        question = (
            "Group X has an average score of 60 and Group Y has an average score of 80. "
            "If both groups initially have 30 members, their combined average is 70. "
            "If 30 additional members are added to Group Y while Group X remains at 30 members, "
            "what will happen to the combined average?"
        )
        correct = "It increases to 73.33 (pulled toward 80)"
        distractors = [
            "It remains unchanged at 70",
            "It decreases toward 60",
            "It increases to 80 exactly",
        ]
        trap_map = {
            "It remains unchanged at 70": "conceptual_mistake",
            "It decreases toward 60": "conceptual_mistake",
            "It increases to 80 exactly": "conceptual_mistake",
        }
        explanation = (
            "Step 1: New sizes: Group X has 30, Group Y has 60 (ratio 1:2).\n"
            "Step 2: Combined average = (1 * 60 + 2 * 80) / 3 = 220 / 3 = 73.33.\n"
            "Step 3: Increasing the relative weight of the higher group pulls the combined average toward 80."
        )

    elif subvariant == "teeter_totter_leverage":
        # Dept A avg 50k, Dept B avg 80k. Combined avg 55k.
        # Dist to A = 5k, Dist to B = 25k. Ratio A:B = 25:5 = 5:1.
        question = (
            "The average annual salary in Division A is $50,000, and in Division B it is $80,000. "
            "If the overall average salary across both divisions combined is $55,000, "
            "what is the ratio of the number of employees in Division A to Division B?"
        )
        correct = "5:1"
        distractors = ["1:5", "1:1", "3:1"]
        trap_map = {
            "1:5": "ratio_interpretation_mistake",
            "1:1": "average_weighted_mistake",
            "3:1": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Teeter-totter principle: Distance to Division A = $55,000 - $50,000 = $5,000.\n"
            "Step 2: Distance to Division B = $80,000 - $55,000 = $25,000.\n"
            "Step 3: The ratio of headcount is inversely proportional to distances:\n"
            "   (Headcount A) / (Headcount B) = 25,000 / 5,000 = 5 / 1 = 5:1."
        )

    elif subvariant == "quick_elimination_bounds":
        # Group 1 avg 62, Group 2 avg 88. Possible combined avg.
        question = (
            "Group 1 has an average score of 62 and Group 2 has an average score of 88. "
            "Regardless of group sizes, which of the following is a possible value for their combined average?"
        )
        correct = "78"
        distractors = ["58", "62", "91"]
        trap_map = {
            "58": "conceptual_mistake",
            "62": "conceptual_mistake",
            "91": "conceptual_mistake",
        }
        explanation = (
            "Step 1: Any weighted average of two distinct groups must lie strictly between their two averages: 62 < Combined Avg < 88.\n"
            "Step 2: 58 is below the minimum (62), 62 would require Group 2 to have 0 members, and 91 is above the maximum (88).\n"
            "Step 3: Only 78 lies strictly within the range (62, 88)."
        )

    else:  # weighted_average_ds_style
        # Men avg 6.0, Women avg 8.5. Combined avg 7.5.
        # Dist to Men = 1.5, Dist to Women = 1.0.
        # Men : Women = 1.0 : 1.5 = 2 : 3. Women fraction = 3/5 = 60%.
        question = (
            "In a satisfaction survey, male customers gave an average score of 6.0 and female customers gave an average score of 8.5. "
            "If the overall average satisfaction score was 7.5, what percentage of the surveyed customers were women?"
        )
        correct = "60%"
        distractors = ["40%", "50%", "75%"]
        trap_map = {
            "40%": "careless_mistake",
            "50%": "average_weighted_mistake",
            "75%": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Distance from male average = |7.5 - 6.0| = 1.5.\n"
            "Step 2: Distance from female average = |8.5 - 7.5| = 1.0.\n"
            "Step 3: Ratio of Men to Women = 1.0 : 1.5 = 2 : 3.\n"
            "Step 4: Percentage of women = 3 / (2 + 3) * 100% = 3/5 * 100% = 60%."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="weighted_average_intuition",
        subvariant=subvariant,
    )

