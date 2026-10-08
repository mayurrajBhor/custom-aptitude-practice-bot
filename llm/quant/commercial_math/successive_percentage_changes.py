import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

from llm.common import GMAT_BENCHMARK_FRACTIONS, clamp_level, make_mcq
from .common import build_mcq, fmt_curr, fmt_num, fmt_pct

def successive_percentage_changes(
    difficulty: int = 2, forced_variant: Optional[str] = None
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "two_increases",
        "increase_then_decrease",
        "symmetric_change_trap",
        "three_successive_changes",
    ]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "two_increases":
        a = random.choice([10, 15, 20, 25, 30, 40])
        b = random.choice([10, 15, 20, 25, 30])
        net = round(a + b + (a * b) / 100, 2)
        correct = fmt_pct(net)
        q_text = f"A share price increases by {a}% in January and then increases by {b}% in February. What is the overall percentage increase?"
        simple_sum = fmt_pct(a + b)
        explanation = (
            f"Step 1: Chain multipliers: (1 + {a}/100) * (1 + {b}/100) = {1 + a/100} * {1 + b/100} = {round((1+a/100)*(1+b/100), 4)}.\n"
            f"Step 2: Subtract 1: {round((1+a/100)*(1+b/100) - 1, 4)} * 100% = {correct}.\n"
            f"Alternatively, use formula a + b + (a*b)/100 = {a} + {b} + {a*b/100} = {correct}.\n"
            f"Trap Warning: Never just add percentages ({simple_sum})! The second increase applies to a larger base."
        )
        distractors = [
            (simple_sum, "conceptual_mistake"),
            (fmt_pct(round(a + b - (a * b) / 100, 2)), "percentage_base_mistake"),
            (fmt_pct(net + 2), "arithmetic_mistake"),
            (fmt_pct(max(1.0, net - 2)), "arithmetic_mistake"),
        ]

    elif variant == "increase_then_decrease":
        a = random.choice([20, 25, 30, 40, 50])
        b = random.choice([10, 15, 20, 25, 30])
        net = round(((1 + a / 100) * (1 - b / 100) - 1) * 100, 2)
        label = "increase" if net > 0 else "decrease"
        correct = f"{abs(net):.2f}% {label}".replace(".00%", "%")
        q_text = f"The price of an asset increases by {a}% and subsequently decreases by {b}%. What is the net percentage change?"
        simple_diff = a - b
        simple_label = "increase" if simple_diff > 0 else "decrease"
        simple_str = f"{abs(simple_diff)}% {simple_label}"
        opp_label = "decrease" if net > 0 else "increase"
        opp_str = f"{abs(net):.2f}% {opp_label}".replace(".00%", "%")

        explanation = (
            f"Step 1: Chain multipliers: (1 + {a}/100) * (1 - {b}/100) = {1 + a/100} * {round(1 - b/100, 2)} = {round((1+a/100)*(1-b/100), 4)}.\n"
            f"Step 2: Net change = {round((1+a/100)*(1-b/100) - 1, 4)} * 100% = {correct}.\n"
            f"Trap: Simple subtraction yields {simple_str}, which ignores the changed base."
        )
        distractors = [
            (simple_str, "conceptual_mistake"),
            (opp_str, "conceptual_mistake"),
            (f"{abs(net) + 3:.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
            (f"{max(1.0, abs(net) - 3):.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
        ]

    elif variant == "symmetric_change_trap":
        x = random.choice([10, 15, 20, 25, 30, 40, 50])
        loss_pct = round((x * x) / 100, 2)
        correct = f"{loss_pct:.2f}% decrease".replace(".00%", "%")
        q_text = (
            f"The price of a commodity increases by {x}% and then decreases by {x}%. "
            f"What is the net percentage change?"
        )
        explanation = (
            f"Step 1: Multiplier chaining: (1 + {x}/100) * (1 - {x}/100) = 1 - ({x}/100)^2 = 1 - {loss_pct/100}.\n"
            f"Step 2: Net change is ALWAYS a decrease of x^2/100 % = {x}^2 / 100 % = {loss_pct}% decrease.\n"
            f"GMAT Trap: Most test-takers fall for '0% (No change)'. Because the decrease is applied to a larger value, the net result is always a loss!"
        )
        distractors = [
            ("0% (No change)", "conceptual_mistake"),
            (f"{loss_pct:.2f}% increase".replace(".00%", "%"), "percentage_base_mistake"),
            (f"{x}% decrease", "careless_mistake"),
            (f"{round(loss_pct + 1, 2)}% decrease", "arithmetic_mistake"),
        ]

    else:  # three_successive_changes
        a = random.choice([10, 20, 25])
        b = random.choice([10, 20])
        c = random.choice([10, 15, 20])
        mult = (1 + a / 100) * (1 - b / 100) * (1 + c / 100)
        net = round((mult - 1) * 100, 2)
        label = "increase" if net >= 0 else "decrease"
        correct = f"{abs(net):.2f}% {label}".replace(".00%", "%")
        q_text = f"A portfolio value changes consecutively by +{a}%, -{b}%, and +{c}%. What is the overall percentage change?"
        simple_sum = a - b + c
        simple_str = f"{abs(simple_sum)}% {'increase' if simple_sum >= 0 else 'decrease'}"
        explanation = (
            f"Step 1: Multiply all 3 factors: (1 + {a/100}) * (1 - {b/100}) * (1 + {c/100}) = {round(mult, 4)}.\n"
            f"Step 2: Overall change = ({round(mult, 4)} - 1) * 100% = {correct}."
        )
        distractors = [
            (simple_str, "conceptual_mistake"),
            (f"{abs(net):.2f}% {'decrease' if label == 'increase' else 'increase'}".replace(".00%", "%"), "conceptual_mistake"),
            (f"{abs(net) + 2:.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
            (f"{max(1.0, abs(net) - 2):.2f}% {label}".replace(".00%", "%"), "arithmetic_mistake"),
        ]

    return build_mcq(
        question=q_text,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        raw_distractors=distractors,
        pattern_name="successive_percentage_changes",
        subvariant=variant,
    )

