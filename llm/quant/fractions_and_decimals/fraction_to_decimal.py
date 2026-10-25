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

def generate_fraction_to_decimal(
    difficulty: int = 2,
    forced_variant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    variants = ["terminating_benchmark", "terminating_advanced", "recurring_fractions"]
    variant = forced_variant if forced_variant in variants else random.choice(variants)

    if variant == "terminating_benchmark":
        benchmarks = [
            (1, 2, "0.5"),
            (1, 4, "0.25"),
            (3, 4, "0.75"),
            (1, 5, "0.2"),
            (2, 5, "0.4"),
            (3, 5, "0.6"),
            (4, 5, "0.8"),
            (1, 8, "0.125"),
            (3, 8, "0.375"),
            (5, 8, "0.625"),
            (7, 8, "0.875"),
        ]
        n, d, correct = random.choice(benchmarks)
        val = float(correct)
        candidates = [
            (f"{val + 0.05:.3g}", "arithmetic_mistake"),
            (f"{val - 0.05:.3g}", "arithmetic_mistake"),
            (f"0.{n}{d}", "conceptual_mistake"),
            (f"{val * 10:.3g}", "formula_selection_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is the decimal equivalent of the fraction {n}/{d}?"
        expl = (
            f"To convert {n}/{d} to a decimal, divide {n} by {d}:\n"
            f"  {n} ÷ {d} = {correct}.\n"
            f"Benchmark recall: {n}/{d} is a standard GMAT benchmark fraction equal to {correct}."
        )

    elif variant == "terminating_advanced":
        advanced = [
            (1, 16, "0.0625"),
            (3, 16, "0.1875"),
            (7, 20, "0.35"),
            (9, 20, "0.45"),
            (11, 25, "0.44"),
            (7, 40, "0.175"),
            (13, 50, "0.26"),
        ]
        n, d, correct = random.choice(advanced)
        val = float(correct)
        candidates = [
            (f"{val / 10:.4g}", "conceptual_mistake"),
            (f"{val * 10:.4g}", "conceptual_mistake"),
            (f"{val + 0.02:.4g}", "arithmetic_mistake"),
            (f"{val - 0.02:.4g}", "arithmetic_mistake"),
        ]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"Convert the fraction {n}/{d} into a terminating decimal."
        expl = (
            f"Divide {n} by {d}:\n"
            f"  {n} ÷ {d} = {correct}."
        )

    else:  # recurring_fractions
        recurring = [
            (1, 3, "0.333...", ["0.3", "0.33", "0.0333..."]),
            (2, 3, "0.666...", ["0.6", "0.66", "0.0666..."]),
            (1, 6, "0.1666...", ["0.16", "0.6", "0.0166..."]),
            (5, 6, "0.8333...", ["0.83", "0.8", "0.0833..."]),
            (1, 9, "0.111...", ["0.1", "0.0111...", "0.9"]),
        ]
        n, d, correct, wrong_opts = random.choice(recurring)
        candidates = [(w, "conceptual_mistake") for w in wrong_opts]
        distractors, trap_map = _clean_distractors(correct, candidates)
        q_text = f"What is the recurring decimal value of {n}/{d}?"
        expl = (
            f"Dividing {n} by {d} yields a repeating (recurring) decimal:\n"
            f"  {n} ÷ {d} = {correct}\n"
            f"Note: Terminating values like {wrong_opts[0]} are rough approximations, not exact representations."
        )

    return make_mcq(
        question=q_text,
        correct=correct,
        explanation=expl,
        difficulty=level,
        distractors=distractors,
        trap_map=trap_map,
        pattern_name="fraction_to_decimal",
        subvariant=variant,
    )

