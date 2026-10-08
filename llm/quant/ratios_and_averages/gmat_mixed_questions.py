from fractions import Fraction
import math
import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import clamp_level, gcd, make_mcq

def generate_gmat_mixed_questions(difficulty: int = 2, forced_variant: Optional[str] = None) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = [
        "ratio_and_percentage",
        "ratio_and_average",
        "percentage_and_profit_loss",
        "fraction_and_percentage_shift",
        "ratio_average_percentage_trio",
    ]
    subvariant = forced_variant if forced_variant in variants else random.choice(variants)

    if subvariant == "ratio_and_percentage":
        # Men : Women = 3 : 2. 20% men certified, 30% women certified.
        # Total certified = (3*20 + 2*30)/5 = (60 + 60)/5 = 24%.
        m, w = 3, 2
        pm, pw = 20, 30
        pct = (m * pm + w * pw) // (m + w)
        question = (
            f"In an engineering firm, the ratio of male to female employees is {m}:{w}. "
            f"If {pm}% of the male employees and {pw}% of the female employees hold professional certifications, "
            f"what percentage of all employees in the firm hold professional certifications?"
        )
        correct = f"{pct}%"
        simple_avg = f"{(pm + pw) // 2}%"
        distractors = [simple_avg, f"{pct + 2}%", f"{pct - 2}%"]
        trap_map = {
            simple_avg: "average_weighted_mistake",
            f"{pct + 2}%": "arithmetic_mistake",
            f"{pct - 2}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Assume a convenient total population based on the ratio {m}:{w}, say {m * 10} males and {w * 10} females (total = {(m + w) * 10}).\n"
            f"Step 2: Certified males = {pm}% of {m * 10} = {m * pm // 10}.\n"
            f"Step 3: Certified females = {pw}% of {w * 10} = {w * pw // 10}.\n"
            f"Step 4: Total certified = {m * pm // 10 + w * pw // 10} out of {(m + w) * 10}.\n"
            f"Step 5: Overall percentage = {pct}%."
        )

    elif subvariant == "ratio_and_average":
        # Box A and B item counts in ratio 2:3. Avg weight in A is 40 kg, in B is 60 kg.
        # Combined avg = (2*40 + 3*60)/5 = (80 + 180)/5 = 260/5 = 52 kg.
        r_a, r_b = 2, 3
        w_a, w_b = 40, 60
        comb_wt = (r_a * w_a + r_b * w_b) // (r_a + r_b)
        question = (
            f"The number of parcels in Warehouse A and Warehouse B is in the ratio {r_a}:{r_b}. "
            f"If the average weight of parcels in Warehouse A is {w_a} kg and in Warehouse B is {w_b} kg, "
            f"what is the average weight of a parcel across both warehouses combined?"
        )
        correct = f"{comb_wt} kg"
        simple_avg = f"{(w_a + w_b) // 2} kg"
        distractors = [simple_avg, f"{comb_wt + 3} kg", f"{comb_wt - 3} kg"]
        trap_map = {
            simple_avg: "average_weighted_mistake",
            f"{comb_wt + 3} kg": "arithmetic_mistake",
            f"{comb_wt - 3} kg": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Weighted average formula = ({r_a} * {w_a} + {r_b} * {w_b}) / ({r_a} + {r_b}).\n"
            f"Step 2: Sum of weighted weights = {r_a * w_a} + {r_b * w_b} = {r_a * w_a + r_b * w_b}.\n"
            f"Step 3: Total ratio parts = {r_a + r_b}.\n"
            f"Step 4: Overall average weight = {r_a * w_a + r_b * w_b} / {r_a + r_b} = {comb_wt} kg."
        )

    elif subvariant == "percentage_and_profit_loss":
        # Markup 40%, Discount 20% -> net profit = 40 - 20 - (40*20)/100 = 12%.
        m_pct = 40
        d_pct = 20
        net_profit = m_pct - d_pct - (m_pct * d_pct) // 100
        question = (
            f"A retailer marks an item {m_pct}% above its original cost price, "
            f"and then offers a discount of {d_pct}% off the marked price. "
            f"What is the retailer's net profit percentage on the cost price?"
        )
        correct = f"{net_profit}%"
        wrong_sub = f"{m_pct - d_pct}%"
        distractors = [wrong_sub, f"{net_profit - 4}%", f"{net_profit + 4}%"]
        trap_map = {
            wrong_sub: "percentage_base_mistake",
            f"{net_profit - 4}%": "arithmetic_mistake",
            f"{net_profit + 4}%": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Let the cost price CP = $100.\n"
            f"Step 2: Marked price MP = $100 * 1.{m_pct} = ${100 + m_pct}.\n"
            f"Step 3: Selling price SP after {d_pct}% discount = ${100 + m_pct} * (1 - {d_pct}/100) = ${100 + m_pct} * 0.8 = ${100 + net_profit}.\n"
            f"Step 4: Net profit = SP - CP = ${100 + net_profit} - $100 = {net_profit}%."
        )

    elif subvariant == "fraction_and_percentage_shift":
        # Increase by 25% (+1/4), then decrease by 20% (-1/5) => net 0% change.
        question = (
            "A company's quarterly stock price increases by 25% in the first quarter, "
            "and then decreases by 20% in the second quarter. "
            "What is the net percentage change in the stock price over the two quarters?"
        )
        correct = "0% (no change)"
        distractors = ["+5% increase", "-5% decrease", "+2.5% increase"]
        trap_map = {
            "+5% increase": "percentage_base_mistake",
            "-5% decrease": "conceptual_mistake",
            "+2.5% increase": "arithmetic_mistake",
        }
        explanation = (
            "Step 1: Let the initial stock price be 100.\n"
            "Step 2: After a 25% increase, the price becomes 100 * 1.25 = 125.\n"
            "Step 3: A 20% decrease on 125 is 125 * 0.20 = 25.\n"
            "Step 4: Final price = 125 - 25 = 100.\n"
            "Step 5: The net percentage change is 0% (the price returns exactly to its starting value)."
        )

    else:  # ratio_average_percentage_trio
        # Ratio 2:2:1, salaries 80k, 60k, 50k -> (160 + 120 + 50)/5 = 330/5 = $66,000.
        r1, r2, r3 = 2, 2, 1
        s1, s2, s3 = 80, 60, 50
        avg_sal = (r1 * s1 + r2 * s2 + r3 * s3) * 1000 // (r1 + r2 + r3)
        question = (
            f"A startup employs engineers, marketers, and administrators in the ratio {r1}:{r2}:{r3}. "
            f"The average annual salaries are ${s1},000 for engineers, ${s2},000 for marketers, and ${s3},000 for administrators. "
            f"What is the company-wide average annual salary per employee?"
        )
        correct = f"${avg_sal:,}"
        unweighted = f"${(s1 + s2 + s3) * 1000 // 3:,}"
        distractors = [unweighted, f"${avg_sal + 4000:,}", f"${avg_sal - 4000:,}"]
        trap_map = {
            unweighted: "average_weighted_mistake",
            f"${avg_sal + 4000:,}": "arithmetic_mistake",
            f"${avg_sal - 4000:,}": "arithmetic_mistake",
        }
        explanation = (
            f"Step 1: Total headcount weight = {r1} + {r2} + {r3} = {r1 + r2 + r3}.\n"
            f"Step 2: Total weighted payroll = ({r1} * ${s1},000) + ({r2} * ${s2},000) + ({r3} * ${s3},000) = ${r1*s1 + r2*s2 + r3*s3},000.\n"
            f"Step 3: Average salary = ${r1*s1 + r2*s2 + r3*s3},000 / {r1 + r2 + r3} = ${avg_sal:,}."
        )

    return make_mcq(
        question=question,
        correct=correct,
        explanation=explanation,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="gmat_mixed_questions",
        subvariant=subvariant,
    )

