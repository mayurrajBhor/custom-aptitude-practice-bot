import math
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

def _format_frac(n: int, d: int) -> str:
    """Formats a fraction n/d, returning integer if d == 1."""
    if d == 1:
        return str(n)
    return f"{n}/{d}"


def _format_mixed(w: int, n: int, d: int) -> str:
    """Formats whole w and proper fraction n/d as a mixed number string."""
    if w == 0:
        return _format_frac(n, d)
    if n == 0:
        return str(w)
    return f"{w} {n}/{d}"


def _clean_distractors(
    correct: str,
    candidates: List[Tuple[str, str]],
) -> Tuple[List[str], Dict[str, str]]:
    """
    Given a correct answer string and a list of (distractor_str, trap_category),
    returns a deduplicated list of non-empty distractors (excluding correct)
    and a corresponding trap_map.
    """
    correct_str = str(correct).strip()
    seen = {correct_str}
    distractors: List[str] = []
    trap_map: Dict[str, str] = {}

    for cand, trap in candidates:
        s = str(cand).strip()
        if s and s not in seen:
            seen.add(s)
            distractors.append(s)
            trap_map[s] = trap

    return distractors, trap_map

