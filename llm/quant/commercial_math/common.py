import random
from typing import Any, Dict, List, Optional, Tuple

from llm.common import make_mcq

def fmt_pct(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"{int(round(val))}%"
    return f"{val:.2f}%"


def fmt_curr(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"${int(round(val))}"
    return f"${val:.2f}"


def fmt_num(val: float) -> str:
    val = round(val, 2)
    if abs(val - round(val)) < 1e-6:
        return f"{int(round(val))}"
    return f"{val:.2f}"


def build_mcq(
    question: str,
    correct: Any,
    explanation: str,
    difficulty: int,
    raw_distractors: List[Tuple[Any, str]],
    pattern_name: str,
    subvariant: str,
) -> Dict[str, Any]:
    correct_str = str(correct).strip()
    distractor_list: List[str] = []
    trap_map: Dict[str, str] = {}

    for val, trap_type in raw_distractors:
        d_str = str(val).strip()
        if d_str and d_str != correct_str and d_str not in distractor_list:
            distractor_list.append(d_str)
            trap_map[d_str] = trap_type

    return make_mcq(
        question=question,
        correct=correct_str,
        explanation=explanation,
        difficulty=difficulty,
        distractors=distractor_list,
        trap_map=trap_map,
        pattern_name=pattern_name,
        subvariant=subvariant,
    )


