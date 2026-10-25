"""Topic: Percentages and Commercial Math (Patterns 5025-5039)."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .percentage_fundamentals import percentage_fundamentals
from .percentage_increase import percentage_increase
from .percentage_decrease import percentage_decrease
from .new_value_percentage_change import new_value_percentage_change
from .reverse_percentage import reverse_percentage
from .successive_percentage_changes import successive_percentage_changes
from .profit_and_loss import profit_and_loss
from .profit_loss_multipliers import profit_loss_multipliers
from .markup import markup
from .discount import discount
from .markup_discount_combined import markup_discount_combined
from .successive_discounts import successive_discounts
from .percentage_vs_percentage_points import percentage_vs_percentage_points
from .more_than_vs_less_than import more_than_vs_less_than
from .percentage_word_problems import percentage_word_problems

generate_percentage_fundamentals = percentage_fundamentals
generate_percentage_increase = percentage_increase
generate_percentage_decrease = percentage_decrease
generate_new_value_percentage_change = new_value_percentage_change
generate_reverse_percentage = reverse_percentage
generate_successive_percentage_changes = successive_percentage_changes
generate_profit_and_loss = profit_and_loss
generate_profit_loss_multipliers = profit_loss_multipliers
generate_markup = markup
generate_discount = discount
generate_markup_discount_combined = markup_discount_combined
generate_successive_discounts = successive_discounts
generate_percentage_vs_percentage_points = percentage_vs_percentage_points
generate_more_than_vs_less_than = more_than_vs_less_than
generate_percentage_word_problems = percentage_word_problems

DAY3_GENERATORS = {
    5025: percentage_fundamentals,
    "5025": percentage_fundamentals,
    "percentage_fundamentals": percentage_fundamentals,
    5026: percentage_increase,
    "5026": percentage_increase,
    "percentage_increase": percentage_increase,
    5027: percentage_decrease,
    "5027": percentage_decrease,
    "percentage_decrease": percentage_decrease,
    5028: new_value_percentage_change,
    "5028": new_value_percentage_change,
    "new_value_percentage_change": new_value_percentage_change,
    5029: reverse_percentage,
    "5029": reverse_percentage,
    "reverse_percentage": reverse_percentage,
    5030: successive_percentage_changes,
    "5030": successive_percentage_changes,
    "successive_percentage_changes": successive_percentage_changes,
    5031: profit_and_loss,
    "5031": profit_and_loss,
    "profit_and_loss": profit_and_loss,
    5032: profit_loss_multipliers,
    "5032": profit_loss_multipliers,
    "profit_loss_multipliers": profit_loss_multipliers,
    5033: markup,
    "5033": markup,
    "markup": markup,
    5034: discount,
    "5034": discount,
    "discount": discount,
    5035: markup_discount_combined,
    "5035": markup_discount_combined,
    "markup_discount_combined": markup_discount_combined,
    5036: successive_discounts,
    "5036": successive_discounts,
    "successive_discounts": successive_discounts,
    5037: percentage_vs_percentage_points,
    "5037": percentage_vs_percentage_points,
    "percentage_vs_percentage_points": percentage_vs_percentage_points,
    5038: more_than_vs_less_than,
    "5038": more_than_vs_less_than,
    "more_than_vs_less_than": more_than_vs_less_than,
    5039: percentage_word_problems,
    "5039": percentage_word_problems,
    "percentage_word_problems": percentage_word_problems,
}

DAY3_PATTERNS_METADATA = {
    5025: {
        "id": 5025,
        "name": "percentage_fundamentals",
        "description": "Find x% of N, what % A is of B, find original number given x% of N = A, and fraction-to-percentage conversions.",
        "variants": [
            "find_percentage_of_number",
            "what_percentage_is_a_of_b",
            "find_base_from_percentage",
            "fraction_to_percentage",
        ],
    },
    5026: {
        "id": 5026,
        "name": "percentage_increase",
        "description": "Percentage increase calculations across price, population, salary, and revenue using original as base.",
        "variants": [
            "price_increase",
            "population_growth",
            "salary_hike",
            "revenue_expansion",
        ],
    },
    5027: {
        "id": 5027,
        "name": "percentage_decrease",
        "description": "Percentage decrease calculations using original value as denominator base.",
        "variants": [
            "price_reduction",
            "population_decline",
            "budget_cut",
            "inventory_depletion",
        ],
    },
    5028: {
        "id": 5028,
        "name": "new_value_percentage_change",
        "description": "Multipliers (1 + r/100) and (1 - r/100) for benchmark and general percentage changes.",
        "variants": [
            "new_value_after_increase",
            "new_value_after_decrease",
            "benchmark_multiplier",
            "multi_step_or_decimal_change",
        ],
    },
    5029: {
        "id": 5029,
        "name": "reverse_percentage",
        "description": "Finding original value from value after percentage change (Original = New / (1 ± r/100)).",
        "variants": [
            "original_price_after_discount",
            "original_salary_after_raise",
            "price_before_sales_tax",
            "original_population_before_change",
        ],
    },
    5030: {
        "id": 5030,
        "name": "successive_percentage_changes",
        "description": "Multiplier chaining for sequential percentage changes and the symmetric +x% / -x% trap.",
        "variants": [
            "two_increases",
            "increase_then_decrease",
            "symmetric_change_trap",
            "three_successive_changes",
        ],
    },
    5031: {
        "id": 5031,
        "name": "profit_and_loss",
        "description": "Cost Price (CP), Selling Price (SP), Profit/Loss amounts and percentages calculated on CP.",
        "variants": [
            "calculate_profit_percentage",
            "calculate_loss_percentage",
            "profit_with_overhead",
            "sp_per_unit_vs_cp",
        ],
    },
    5032: {
        "id": 5032,
        "name": "profit_loss_multipliers",
        "description": "Direct profit and loss multipliers: SP = CP(1 ± r/100) and finding CP = SP / (1 ± r/100).",
        "variants": [
            "find_sp_from_cp_and_profit",
            "find_sp_from_cp_and_loss",
            "find_cp_from_sp_and_profit",
            "find_cp_from_sp_and_loss",
        ],
    },
    5033: {
        "id": 5033,
        "name": "markup",
        "description": "Marked price from cost price and markup percentage, and markup vs profit margin distinction.",
        "variants": [
            "calculate_marked_price",
            "calculate_markup_percentage",
            "find_cost_price_from_markup",
            "markup_vs_margin",
        ],
    },
    5034: {
        "id": 5034,
        "name": "discount",
        "description": "Discounts and discount percentages calculated on Marked Price (MP), and finding SP/MP.",
        "variants": [
            "calculate_discount_percentage",
            "find_selling_price_after_discount",
            "find_marked_price_from_discount",
            "discount_amount_from_percentage",
        ],
    },
    5035: {
        "id": 5035,
        "name": "markup_discount_combined",
        "description": "CP -> markup -> MP -> discount -> SP and net profit/loss percentage calculations.",
        "variants": [
            "find_net_profit_percentage",
            "find_sp_and_profit_given_cp",
            "breakeven_discount",
            "find_markup_needed_for_target_profit",
        ],
    },
    5036: {
        "id": 5036,
        "name": "successive_discounts",
        "description": "Successive discount chaining MP * (1 - d1) * (1 - d2) and eliminating simple addition trap.",
        "variants": [
            "two_successive_discounts_equivalent",
            "final_sp_after_two_discounts",
            "compare_discount_schemes",
            "three_successive_discounts",
        ],
    },
    5037: {
        "id": 5037,
        "name": "percentage_vs_percentage_points",
        "description": "Trap distinction between change in percentage points and relative percentage change.",
        "variants": [
            "percentage_points_vs_percent_increase",
            "percentage_points_vs_percent_decrease",
            "interest_rate_change",
            "identify_correct_statement",
        ],
    },
    5038: {
        "id": 5038,
        "name": "more_than_vs_less_than",
        "description": "Relative percentage comparisons: 'A is what % more than B' vs 'B is what % less than A'.",
        "variants": [
            "a_more_than_b_direct",
            "b_less_than_a_direct",
            "a_is_x_percent_more_then_b_is_what_less",
            "a_is_x_percent_less_then_b_is_what_more",
        ],
    },
    5039: {
        "id": 5039,
        "name": "percentage_word_problems",
        "description": "Multi-step GMAT applications: demographics, remainder budgets, exam pass thresholds, and growth.",
        "variants": [
            "demographics_and_subgroups",
            "salary_and_remainder_budget",
            "exam_score_and_passing_threshold",
            "revenue_cost_profit_growth",
        ],
    },
}


class CommercialMathMixin:
    """Mixin exposing Commercial Math generators."""
    percentage_fundamentals = staticmethod(percentage_fundamentals)
    percentage_increase = staticmethod(percentage_increase)
    percentage_decrease = staticmethod(percentage_decrease)
    new_value_percentage_change = staticmethod(new_value_percentage_change)
    reverse_percentage = staticmethod(reverse_percentage)
    successive_percentage_changes = staticmethod(successive_percentage_changes)
    profit_and_loss = staticmethod(profit_and_loss)
    profit_loss_multipliers = staticmethod(profit_loss_multipliers)
    markup = staticmethod(markup)
    discount = staticmethod(discount)
    markup_discount_combined = staticmethod(markup_discount_combined)
    successive_discounts = staticmethod(successive_discounts)
    percentage_vs_percentage_points = staticmethod(percentage_vs_percentage_points)
    more_than_vs_less_than = staticmethod(more_than_vs_less_than)
    percentage_word_problems = staticmethod(percentage_word_problems)


__all__ = [
    "DAY3_GENERATORS",
    "DAY3_PATTERNS_METADATA",
    "CommercialMathMixin",
    "percentage_fundamentals",
    "percentage_increase",
    "percentage_decrease",
    "new_value_percentage_change",
    "reverse_percentage",
    "successive_percentage_changes",
    "profit_and_loss",
    "profit_loss_multipliers",
    "markup",
    "discount",
    "markup_discount_combined",
    "successive_discounts",
    "percentage_vs_percentage_points",
    "more_than_vs_less_than",
    "percentage_word_problems",
    "generate_percentage_fundamentals",
    "generate_percentage_increase",
    "generate_percentage_decrease",
    "generate_new_value_percentage_change",
    "generate_reverse_percentage",
    "generate_successive_percentage_changes",
    "generate_profit_and_loss",
    "generate_profit_loss_multipliers",
    "generate_markup",
    "generate_discount",
    "generate_markup_discount_combined",
    "generate_successive_discounts",
    "generate_percentage_vs_percentage_points",
    "generate_more_than_vs_less_than",
    "generate_percentage_word_problems",
]
