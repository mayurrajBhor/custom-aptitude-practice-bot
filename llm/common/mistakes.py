from typing import Any, Dict, Optional

MISTAKE_CATEGORIES = {
    "conceptual_mistake": {
        "label": "Conceptual Mistake",
        "description": "Misunderstanding a core mathematical definition, classification rule, or mathematical principle.",
        "remedy": "Review fundamental definitions, boundary conditions (such as 0, 1, negatives), and underlying theorems.",
    },
    "formula_selection_mistake": {
        "label": "Formula Selection Mistake",
        "description": "Selected or applied an inappropriate formula for the given relationship.",
        "remedy": "Identify the given relationships first before picking a formula (e.g. Keep-Change-Flip for division).",
    },
    "setup_mistake": {
        "label": "Setup Mistake",
        "description": "Algebraic translation or structural equation setup was misaligned.",
        "remedy": "Write clear variable equations (such as A = mx, B = nx) before performing algebra.",
    },
    "arithmetic_mistake": {
        "label": "Arithmetic Mistake",
        "description": "Basic arithmetic calculation or computation slip.",
        "remedy": "Double-check intermediate calculations or verify using estimation / unit-digit checking.",
    },
    "sign_mistake": {
        "label": "Sign Mistake",
        "description": "Flipped positive/negative signs or misinterpreted direction of change.",
        "remedy": "Track signs carefully at each step, especially in negatives and subtraction operations.",
    },
    "ratio_interpretation_mistake": {
        "label": "Ratio Interpretation Mistake",
        "description": "Treated ratio values as absolute physical quantities rather than proportional parts.",
        "remedy": "Always introduce a scale factor (x) when working with ratios (A = mx, B = nx).",
    },
    "percentage_base_mistake": {
        "label": "Percentage Base Mistake",
        "description": "Divided by the wrong denominator base anchor (e.g., using SP instead of CP, or New instead of Original).",
        "remedy": "Remember: Profit/Loss % is always on CP, Discount % on MP, and % Change on Original.",
    },
    "average_weighted_mistake": {
        "label": "Weighted Average Mistake",
        "description": "Treated unequal groups as simple arithmetic averages instead of weighting by counts.",
        "remedy": "Use total sum / total count. The combined average is always pulled toward the larger group.",
    },
    "calculation_speed_mistake": {
        "label": "Speed / Timeout Mistake",
        "description": "Ran out of time or made a hasty guess under time pressure.",
        "remedy": "Practice lightning drills and mental shortcuts to avoid tedious scratchpad calculations.",
    },
    "careless_mistake": {
        "label": "Careless Mistake",
        "description": "Inverted terms or solved for the wrong variable (e.g. A more than B vs B less than A).",
        "remedy": "Carefully re-read the final question prompt to confirm exactly what quantity is being asked.",
    },
}


def classify_mistake(
    question_dict: Dict[str, Any],
    selected_option: Optional[str] = None,
    is_timeout: bool = False,
    time_taken_seconds: float = 0.0,
) -> Dict[str, str]:
    if is_timeout:
        info = MISTAKE_CATEGORIES["calculation_speed_mistake"]
        return {
            "category": "calculation_speed_mistake",
            "label": info["label"],
            "feedback": "You ran out of time on this question.",
            "remedy": info["remedy"],
        }

    trap_map = question_dict.get("trap_map", {})
    if selected_option and selected_option in trap_map:
        category = trap_map[selected_option]
        if category in MISTAKE_CATEGORIES:
            info = MISTAKE_CATEGORIES[category]
            return {
                "category": category,
                "label": info["label"],
                "feedback": f"Common trap triggered: {info['description']}",
                "remedy": info["remedy"],
            }

    # Heuristic matching based on pattern name or wording
    pattern = str(question_dict.get("pattern_name", "")).lower()
    text = str(question_dict.get("question_text", "")).lower()

    if any(k in pattern or k in text for k in ["profit", "loss", "markup", "discount", "percent", "percentage"]):
        if any(k in pattern or k in text for k in ["profit", "discount", "more than", "less than"]):
            category = "percentage_base_mistake"
        else:
            category = "conceptual_mistake"
    elif any(k in pattern or k in text for k in ["ratio", "proportion"]):
        category = "ratio_interpretation_mistake"
    elif any(k in pattern or k in text for k in ["average", "weighted"]):
        category = "average_weighted_mistake"
    elif any(k in pattern or k in text for k in ["sign", "negative", "integer"]):
        category = "sign_mistake"
    elif any(k in pattern or k in text for k in ["prime", "parity", "odd", "even", "natural", "whole"]):
        category = "conceptual_mistake"
    elif any(k in pattern or k in text for k in ["bodmas", "pemdas", "order of operations"]):
        category = "formula_selection_mistake"
    else:
        category = "arithmetic_mistake"

    info = MISTAKE_CATEGORIES[category]
    return {
        "category": category,
        "label": info["label"],
        "feedback": info["description"],
        "remedy": info["remedy"],
    }
