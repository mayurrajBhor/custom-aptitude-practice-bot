from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_inverse_proportion(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "workers_and_days",
        "speed_and_time",
        "pipes_or_machines",
        "provisions_and_people",
        "gear_teeth_revolutions",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "workers_and_days":
        # w1 * d1 = w2 * d2
        w1 = random.choice([6, 8, 10, 12])
        d1 = random.choice([12, 15, 20, 24])
        total_work = w1 * d1
        # Pick w2 divisor of total_work
        factors = [f for f in range(3, total_work) if total_work % f == 0 and f != w1]
        w2 = random.choice(factors[:6])
        d2 = total_work // w2
        question = (
            f"{w1} workers can complete a construction job in {d1} days working at identical rates. "
            f"How many days will {w2} workers take to complete the same job?"
        )
        correct = f"{d2} days"
        wrong_direct = f"{int((w2 * d1) / w1)} days"
        distractors = [wrong_direct, f"{d2 + 2} days", f"{max(1, d2 - 2)} days"]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            f"{d2 + 2} days": "arithmetic_mistake",
            f"{max(1, d2 - 2)} days": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Workers and days are inversely proportional: Total Worker-Days = w1 * d1 = {w1} * {d1} = {total_work}.\n"
            f"Step 2: For {w2} workers: {w2} * d2 = {total_work}.\n"
            f"Step 3: d2 = {total_work} / {w2} = {d2} days."
        )

    elif subvariant == "speed_and_time":
        s1 = random.choice([40, 50, 60, 75])
        t1 = random.choice([3, 4, 5, 6])
        distance = s1 * t1
        factors = [f for f in range(2, 10) if distance % f == 0 and f != t1]
        t2 = random.choice(factors)
        s2 = distance // t2
        question = (
            f"A motorist traveling at an average speed of {s1} km/h completes a journey in {t1} hours. "
            f"What average speed must the motorist maintain to complete the same journey in {t2} hours?"
        )
        correct = f"{s2} km/h"
        wrong_direct = f"{int((s1 * t2) / t1)} km/h"
        distractors = [wrong_direct, f"{s2 + 5} km/h", f"{s2 - 5} km/h"]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            f"{s2 + 5} km/h": "arithmetic_mistake",
            f"{s2 - 5} km/h": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total distance = speed * time = {s1} km/h * {t1} hours = {distance} km.\n"
            f"Step 2: Required speed for {t2} hours = Distance / {t2} = {distance} / {t2} = {s2} km/h."
        )

    elif subvariant == "pipes_or_machines":
        m1 = random.choice([4, 6, 8])
        h1 = random.choice([6, 9, 12])
        total_machine_hours = m1 * h1
        factors = [f for f in range(2, 15) if total_machine_hours % f == 0 and f != h1]
        h2 = random.choice(factors)
        m2 = total_machine_hours // h2
        question = (
            f"{m1} identical industrial printing machines can finish a bulk printing order in {h1} hours. "
            f"How many of these machines are needed to complete the order in {h2} hours?"
        )
        correct = str(m2)
        wrong_direct = str(int((m1 * h2) / h1))
        distractors = [wrong_direct, str(m2 + 1), str(max(1, m2 - 1))]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            str(m2 + 1): "arithmetic_mistake",
            str(max(1, m2 - 1)): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total machine-hours required = {m1} * {h1} = {total_machine_hours}.\n"
            f"Step 2: Number of machines required = Total machine-hours / {h2} = {total_machine_hours} / {h2} = {m2}."
        )

    elif subvariant == "provisions_and_people":
        p1 = random.choice([30, 40, 50, 60])
        d1 = random.choice([20, 25, 30])
        tot_person_days = p1 * d1
        # Add people
        p_extra = random.choice([10, 20])
        p2 = p1 + p_extra
        d2 = tot_person_days // p2
        # adjust to exact division
        tot_person_days = p2 * d2
        d1 = tot_person_days // p1
        question = (
            f"A military post has sufficient food supplies for {p1} soldiers for {d1} days. "
            f"If {p_extra} additional soldiers join the post, how many days will the supplies last?"
        )
        correct = f"{d2} days"
        distractors = [f"{d1 - p_extra} days", f"{int(d1 * p2 / p1)} days", f"{d2 + 3} days"]
        trap_map = {
            f"{d1 - p_extra} days": "conceptual_mistake",
            f"{int(d1 * p2 / p1)} days": "formula_selection_mistake",
            f"{d2 + 3} days": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total rations = {p1} soldiers * {d1} days = {tot_person_days} person-days.\n"
            f"Step 2: New group size = {p1} + {p_extra} = {p2} soldiers.\n"
            f"Step 3: Days supplies will last = {tot_person_days} / {p2} = {d2} days."
        )

    else:  # gear_teeth_revolutions
        t1, r1, t2, r2 = random.choice([
            (20, 15, 30, 10),
            (24, 10, 40, 6),
            (16, 25, 40, 10),
            (18, 20, 24, 15),
        ])
        question = (
            f"Gear A has {t1} teeth and meshes with Gear B which has {t2} teeth. "
            f"When Gear A makes {r1} complete revolutions, how many revolutions does Gear B make?"
        )
        correct = str(r2)
        wrong_direct = str(int((t2 * r1) / t1))
        distractors = [wrong_direct, str(r2 + 2), str(max(1, r2 - 2))]
        trap_map = {
            wrong_direct: "formula_selection_mistake",
            str(r2 + 2): "arithmetic_mistake",
            str(max(1, r2 - 2)): "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: The number of teeth passing the contact point is constant: teeth * revolutions = constant.\n"
            f"Step 2: {t1} * {r1} = {t1 * r1}.\n"
            f"Step 3: Gear B revolutions = ({t1} * {r1}) / {t2} = {t1 * r1} / {t2} = {r2} revolutions."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="inverse_proportion",
        subvariant=subvariant,
    )

