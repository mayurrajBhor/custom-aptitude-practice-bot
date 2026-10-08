import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

from llm.common import (
    GMAT_BENCHMARK_FRACTIONS,
    clamp_level,
    gcd,
    lcm,
    make_mcq,
    make_options,
)
from .common import _clean_distractors, _format_frac, _format_mixed

def generate_fraction_to_percentage(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["fraction_to_percent", "percent_to_fraction", "improper_fraction_to_percent"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    benchmarks = [
        (1, 2, "50%"),
        (1, 3, "33.33%"),
        (2, 3, "66.67%"),
        (1, 4, "25%"),
        (3, 4, "75%"),
        (1, 5, "20%"),
        (2, 5, "40%"),
        (3, 5, "60%"),
        (4, 5, "80%"),
        (1, 6, "16.67%"),
        (5, 6, "83.33%"),
        (1, 8, "12.5%"),
        (3, 8, "37.5%"),
        (5, 8, "62.5%"),
        (7, 8, "87.5%"),
        (1, 10, "10%"),
    ]

    if variant == "fraction_to_percent":
        n, d, pct = random.choice(benchmarks)
        correct = pct
        val = float(pct.replace("%", ""))

        candidates = [
            (f"{val / 10:.2f}%", "conceptual_mistake"),
            (f"{val * 10:.1f}%", "conceptual_mistake"),
            (f"{val + 5:.2f}%".replace(".00%", "%"), "arithmetic_mistake"),
            ("14.28%" if pct != "14.28%" else "12.5%", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the benchmark fraction {n}/{d} into a percentage."
        expl = (
            f"Step 1: Multiply the fraction by 100%:\n"
            f"  ({n}/{d}) × 100% = {n * 100}/{d}% = {correct}.\n"
            f"Memorizing benchmark fractions ({n}/{d} = {correct}) is essential for GMAT quant speed."
        )

    elif variant == "percent_to_fraction":
        n, d, pct = random.choice(benchmarks)
        correct = f"{n}/{d}"

        candidates = [
            (f"{d}/{n}", "careless_mistake"),
            (f"{n + 1}/{d}", "arithmetic_mistake"),
            (f"{n}/{d + 1}", "arithmetic_mistake"),
            (f"{n}/{d * 2}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert {pct} into a fraction in simplest terms."
        expl = (
            f"Step 1: Express {pct} as a fraction over 100.\n"
            f"Step 2: Recognize the benchmark table equivalent: {pct} = {correct}."
        )

    else:  # improper_fraction_to_percent
        impropers = [
            (5, 4, "125%"),
            (3, 2, "150%"),
            (7, 5, "140%"),
            (4, 3, "133.33%"),
            (9, 8, "112.5%"),
        ]
        n, d, correct = random.choice(impropers)
        val = float(correct.replace("%", ""))
        candidates = [
            (f"{val - 100}%", "careless_mistake"),
            (f"{val / 10}%", "conceptual_mistake"),
            (f"{val + 10}%", "arithmetic_mistake"),
            ("100%", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the improper fraction {n}/{d} into a percentage."
        expl = (
            f"Step 1: Multiply by 100%: ({n}/{d}) × 100% = {n * 100}/{d}% = {correct}.\n"
            f"Notice that since {n} > {d}, the percentage must exceed 100%."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_to_percentage",
        subvariant=variant,
    )

