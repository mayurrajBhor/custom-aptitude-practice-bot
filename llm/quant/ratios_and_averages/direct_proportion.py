from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_direct_proportion(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "items_and_cost",
        "distance_and_fuel",
        "hours_and_production",
        "weight_and_price",
        "speed_constant_time",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "items_and_cost":
        unit_cost = random.randint(4, 18)
        n1 = random.randint(3, 8)
        c1 = n1 * unit_cost
        n2 = random.randint(9, 20)
        c2 = n2 * unit_cost
        question = (
            f"If {n1} identical notebooks cost a total of ${c1}, "
            f"what is the cost of {n2} of these notebooks?"
        )
        correct = f"${c2}"
        distractors = [f"${c2 - unit_cost}", f"${c2 + unit_cost}", f"${int((n1 * c1) / n2)}"]
        trap_map = {
            f"${c2 - unit_cost}": "arithmetic_mistake",
            f"${c2 + unit_cost}": "arithmetic_mistake",
            f"${int((n1 * c1) / n2)}": "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Find unit cost: ${c1} / {n1} = ${unit_cost} per notebook.\n"
            f"Step 2: Multiply by new quantity: {n2} * ${unit_cost} = ${c2}."
        )

    elif subvariant == "distance_and_fuel":
        km_per_liter = random.choice([12, 14, 15, 16, 18])
        f1 = random.randint(3, 6)
        d1 = f1 * km_per_liter
        f2 = random.randint(7, 15)
        d2 = f2 * km_per_liter
        question = (
            f"A car travels {d1} kilometers on {f1} liters of petrol. "
            f"Assuming the consumption rate remains constant, how many kilometers can it travel on {f2} liters?"
        )
        correct = f"{d2} km"
        distractors = [f"{d2 - km_per_liter} km", f"{d2 + km_per_liter} km", f"{int(d1 * f1 / f2)} km"]
        trap_map = {
            f"{d2 - km_per_liter} km": "arithmetic_mistake",
            f"{d2 + km_per_liter} km": "arithmetic_mistake",
            f"{int(d1 * f1 / f2)} km": "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Calculate fuel economy: {d1} km / {f1} L = {km_per_liter} km/L.\n"
            f"Step 2: Distance on {f2} liters = {f2} * {km_per_liter} = {d2} km."
        )

    elif subvariant == "hours_and_production":
        rate = random.randint(25, 60)
        h1 = random.randint(2, 5)
        p1 = h1 * rate
        h2 = h1 + random.randint(3, 6)
        p2 = h2 * rate
        question = (
            f"An automated packaging machine produces {p1} packages in {h1} hours. "
            f"At this consistent rate, how many packages will it produce in {h2} hours?"
        )
        correct = str(p2)
        distractors = [str(p2 - rate), str(p2 + rate), str(int(p1 * h1 / h2))]
        trap_map = {
            str(p2 - rate): "arithmetic_mistake",
            str(p2 + rate): "arithmetic_mistake",
            str(int(p1 * h1 / h2)): "formula_selection_mistake",
        }
        explanation = (
            f"Step 1: Production rate = {p1} packages / {h1} hours = {rate} packages/hour.\n"
            f"Step 2: Output in {h2} hours = {h2} * {rate} = {p2} packages."
        )

    elif subvariant == "weight_and_price":
        price_per_kg = random.randint(15, 45)
        w1 = random.choice([2, 4, 5])
        c1 = w1 * price_per_kg
        w2 = w1 + random.choice([3, 5, 7])
        c2 = w2 * price_per_kg
        question = (
            f"The cost of copper cable is directly proportional to its weight. "
            f"If a roll weighing {w1} kg costs ${c1}, how much does a roll weighing {w2} kg cost?"
        )
        correct = f"${c2}"
        distractors = [f"${c2 - price_per_kg}", f"${c2 + price_per_kg}", f"${c1 + w2}"]
        trap_map = {
            f"${c2 - price_per_kg}": "arithmetic_mistake",
            f"${c2 + price_per_kg}": "arithmetic_mistake",
            f"${c1 + w2}": "setup_mistake",
        }
        explanation = (
            f"Step 1: Cost per kg = ${c1} / {w1} = ${price_per_kg} per kg.\n"
            f"Step 2: Cost for {w2} kg = {w2} * ${price_per_kg} = ${c2}."
        )

    else:  # speed_constant_time
        time_hrs = random.choice([2, 3, 4])
        s1 = random.choice([40, 50, 60])
        d1 = s1 * time_hrs
        s2 = s1 + random.choice([15, 20, 30])
        d2 = s2 * time_hrs
        question = (
            f"In a fixed duration of time, a train covers {d1} miles traveling at {s1} mph. "
            f"If the train increases its speed to {s2} mph, how many miles will it cover in the same duration?"
        )
        correct = f"{d2} miles"
        distractors = [f"{d1} miles", f"{int(d1 * s1 / s2)} miles", f"{d2 + 10} miles"]
        trap_map = {
            f"{d1} miles": "conceptual_mistake",
            f"{int(d1 * s1 / s2)} miles": "formula_selection_mistake",
            f"{d2 + 10} miles": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Time = Distance / Speed = {d1} / {s1} = {time_hrs} hours.\n"
            f"Step 2: Distance at {s2} mph = {time_hrs} * {s2} = {d2} miles."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="direct_proportion",
        subvariant=subvariant,
    )

