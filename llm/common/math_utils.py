import random
import math
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union

GMAT_BENCHMARK_FRACTIONS = [
    (1, 2, "50%", 0.5),
    (1, 3, "33.33%", 0.3333),
    (1, 4, "25%", 0.25),
    (1, 5, "20%", 0.20),
    (1, 6, "16.67%", 0.1667),
    (1, 7, "14.28%", 0.1428),
    (1, 8, "12.5%", 0.125),
    (1, 9, "11.11%", 0.1111),
    (1, 10, "10%", 0.10),
    (1, 11, "9.09%", 0.0909),
    (1, 12, "8.33%", 0.0833),
    (1, 16, "6.25%", 0.0625),
    (1, 20, "5%", 0.05),
    (1, 25, "4%", 0.04),
    (1, 50, "2%", 0.02),
    (3, 8, "37.5%", 0.375),
    (5, 8, "62.5%", 0.625),
    (7, 8, "87.5%", 0.875),
    (2, 3, "66.67%", 0.6667),
    (3, 4, "75%", 0.75),
    (4, 5, "80%", 0.80),
    (5, 6, "83.33%", 0.8333),
]


def clamp_level(difficulty: Any) -> int:
    try:
        level = int(round(float(difficulty)))
    except (TypeError, ValueError):
        level = 1
    return max(1, min(5, level))


def make_options(correct: Any, distractors: Optional[List[Any]] = None) -> Tuple[List[str], int]:
    correct_str = str(correct).strip()
    options: List[str] = [correct_str]
    seen = {correct_str}

    if distractors:
        for d in distractors:
            d_str = str(d).strip()
            if d_str and d_str not in seen:
                options.append(d_str)
                seen.add(d_str)
            if len(options) == 4:
                break

    # Fill up to 4 options if not enough plausible distractors provided
    delta = 1
    while len(options) < 4:
        cand = None
        try:
            val = float(correct_str.replace("%", "").replace("$", "").replace(" units", "").strip())
            cand_val = int(round(val)) + delta if val.is_integer() else round(val + delta * 0.5, 2)
            if "%" in correct_str:
                cand = f"{cand_val}%"
            elif "$" in correct_str:
                cand = f"${cand_val}"
            else:
                cand = str(cand_val)
        except ValueError:
            cand = f"Choice {chr(65 + len(options))}"

        if cand and cand not in seen:
            options.append(cand)
            seen.add(cand)
        delta = -delta if delta > 0 else (-delta + 1)

    random.shuffle(options)
    return options, options.index(correct_str)


def make_mcq(
    question: str,
    correct: Any,
    explanation: str,
    difficulty: int = 2,
    distractors: Optional[List[Any]] = None,
    trap_map: Optional[Dict[str, str]] = None,
    pattern_name: Optional[str] = None,
    subvariant: Optional[str] = None,
) -> Dict[str, Any]:
    level = clamp_level(difficulty)
    options, index = make_options(correct, distractors)
    return {
        "question_text": question,
        "options": options,
        "correct_option_index": index,
        "explanation": explanation,
        "difficulty": level,
        "trap_map": trap_map or {},
        "pattern_name": pattern_name or "",
        "subvariant": subvariant or "",
    }


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def get_prime_factors(n: int) -> Dict[int, int]:
    factors: Dict[int, int] = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def gcd(a: int, b: int) -> int:
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def lcm_list(numbers: List[int]) -> int:
    res = 1
    for num in numbers:
        res = lcm(res, num)
    return res


def get_all_divisors(n: int) -> List[int]:
    divs = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i * i != n:
                divs.append(n // i)
    return sorted(divs)


def format_fraction_latex(frac: Fraction) -> str:
    if frac.denominator == 1:
        return str(frac.numerator)
    return f"{frac.numerator}/{frac.denominator}"
