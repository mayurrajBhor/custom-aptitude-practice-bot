"""Topic: Ratios, Proportion and Averages (Patterns 5040-5055)."""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .ratio_basics import generate_ratio_basics
from .ratio_with_total import generate_ratio_with_total
from .ratio_one_value_known import generate_ratio_one_value_known
from .ratio_changes import generate_ratio_changes
from .ratio_variables_x_method import generate_ratio_variables_x_method
from .proportion import generate_proportion
from .direct_proportion import generate_direct_proportion
from .inverse_proportion import generate_inverse_proportion
from .average_basics import generate_average_basics
from .missing_number_average import generate_missing_number_average
from .adding_number_to_average import generate_adding_number_to_average
from .removing_number_from_average import generate_removing_number_from_average
from .average_change_shortcut import generate_average_change_shortcut
from .weighted_average import generate_weighted_average
from .weighted_average_intuition import generate_weighted_average_intuition
from .gmat_mixed_questions import generate_gmat_mixed_questions

DAY4_PATTERNS_METADATA: Dict[Any, Dict[str, Any]] = {
    5040: {
        "id": 5040,
        "name": "ratio_basics",
        "description": "Interpret, simplify, equivalent ratios, compare, convert to actual quantities.",
        "variants": [
            "interpret_ratio",
            "simplify_ratio",
            "equivalent_ratios",
            "compare_ratios",
            "convert_to_actual",
        ],
        "variant_names": [
            "interpret_ratio",
            "simplify_ratio",
            "equivalent_ratios",
            "compare_ratios",
            "convert_to_actual",
        ],
    },
    5041: {
        "id": 5041,
        "name": "ratio_with_total",
        "description": "Divide a total amount among parts using given ratios.",
        "variants": [
            "two_parts_find_one",
            "two_parts_difference",
            "three_parts_find_one",
            "three_parts_extremes_diff",
            "ratio_with_total_word_problem",
        ],
        "variant_names": [
            "two_parts_find_one",
            "two_parts_difference",
            "three_parts_find_one",
            "three_parts_extremes_diff",
            "ratio_with_total_word_problem",
        ],
    },
    5042: {
        "id": 5042,
        "name": "ratio_one_value_known",
        "description": "Calculate missing parts, totals, or differences when one ratio value is known.",
        "variants": [
            "first_known_find_second",
            "second_known_find_first",
            "one_known_find_total",
            "one_known_find_difference",
            "three_way_one_known",
        ],
        "variant_names": [
            "first_known_find_second",
            "second_known_find_first",
            "one_known_find_total",
            "one_known_find_difference",
            "three_way_one_known",
        ],
    },
    5043: {
        "id": 5043,
        "name": "ratio_changes",
        "description": "Analyze ratio shifts when quantities are added, removed, or transferred.",
        "variants": [
            "add_to_one_part",
            "remove_from_one_part",
            "ratio_becomes_equal",
            "add_to_both_parts",
            "remove_from_both_parts",
        ],
        "variant_names": [
            "add_to_one_part",
            "remove_from_one_part",
            "ratio_becomes_equal",
            "add_to_both_parts",
            "remove_from_both_parts",
        ],
    },
    5044: {
        "id": 5044,
        "name": "ratio_variables_x_method",
        "description": "Algebraic x-multiplier method for ratios with sums, differences, products, and squares.",
        "variants": [
            "linear_relation_x",
            "difference_given_x",
            "sum_of_squares_x",
            "product_given_x",
            "consecutive_ratio_equations",
        ],
        "variant_names": [
            "linear_relation_x",
            "difference_given_x",
            "sum_of_squares_x",
            "product_given_x",
            "consecutive_ratio_equations",
        ],
    },
    5045: {
        "id": 5045,
        "name": "proportion",
        "description": "Direct scale factor, cross-multiplication, fourth, third, and mean proportionals.",
        "variants": [
            "fourth_proportional",
            "mean_proportional",
            "third_proportional",
            "cross_multiplication_algebra",
            "scale_factor_proportion",
        ],
        "variant_names": [
            "fourth_proportional",
            "mean_proportional",
            "third_proportional",
            "cross_multiplication_algebra",
            "scale_factor_proportion",
        ],
    },
    5046: {
        "id": 5046,
        "name": "direct_proportion",
        "description": "Direct variation relationships: cost, fuel consumption, and production output.",
        "variants": [
            "items_and_cost",
            "distance_and_fuel",
            "hours_and_production",
            "weight_and_price",
            "speed_constant_time",
        ],
        "variant_names": [
            "items_and_cost",
            "distance_and_fuel",
            "hours_and_production",
            "weight_and_price",
            "speed_constant_time",
        ],
    },
    5047: {
        "id": 5047,
        "name": "inverse_proportion",
        "description": "Inverse variation relationships: workers & days, speed & time, and equipment.",
        "variants": [
            "workers_and_days",
            "speed_and_time",
            "pipes_or_machines",
            "provisions_and_people",
            "gear_teeth_revolutions",
        ],
        "variant_names": [
            "workers_and_days",
            "speed_and_time",
            "pipes_or_machines",
            "provisions_and_people",
            "gear_teeth_revolutions",
        ],
    },
    5048: {
        "id": 5048,
        "name": "average_basics",
        "description": "Fundamental arithmetic mean calculations, total sum derivation, and consecutive sequence averages.",
        "variants": [
            "compute_average",
            "find_sum_from_average",
            "find_count_from_sum_and_avg",
            "average_of_consecutive_integers",
            "average_of_multiples",
        ],
        "variant_names": [
            "compute_average",
            "find_sum_from_average",
            "find_count_from_sum_and_avg",
            "average_of_consecutive_integers",
            "average_of_multiples",
        ],
    },
    5049: {
        "id": 5049,
        "name": "missing_number_average",
        "description": "Determine missing elements given group averages, targets, or inter-element relationships.",
        "variants": [
            "one_missing_in_set",
            "test_score_target",
            "consecutive_series_with_unknown",
            "two_missing_with_relation",
            "missing_sales_or_daily_target",
        ],
        "variant_names": [
            "one_missing_in_set",
            "test_score_target",
            "consecutive_series_with_unknown",
            "two_missing_with_relation",
            "missing_sales_or_daily_target",
        ],
    },
    5050: {
        "id": 5050,
        "name": "adding_number_to_average",
        "description": "Compute updated group averages or identify added values when new items or members join.",
        "variants": [
            "find_new_average_one_added",
            "find_added_value",
            "teacher_joins_class",
            "batsman_or_player_score",
            "multiple_items_added",
        ],
        "variant_names": [
            "find_new_average_one_added",
            "find_added_value",
            "teacher_joins_class",
            "batsman_or_player_score",
            "multiple_items_added",
        ],
    },
    5051: {
        "id": 5051,
        "name": "removing_number_from_average",
        "description": "Analyze shifts in average when elements are removed or replaced in a dataset.",
        "variants": [
            "find_new_average_one_removed",
            "find_removed_value",
            "student_leaves_group",
            "replacement_in_average",
            "multiple_items_removed",
        ],
        "variant_names": [
            "find_new_average_one_removed",
            "find_removed_value",
            "student_leaves_group",
            "replacement_in_average",
            "multiple_items_removed",
        ],
    },
    5052: {
        "id": 5052,
        "name": "average_change_shortcut",
        "description": "Apply net deviation shortcuts to rapidly solve average change and replacement questions.",
        "variants": [
            "find_added_via_deviation",
            "find_removed_via_deviation",
            "find_replacement_diff",
            "find_count_via_deviation",
            "sum_of_deviations_zero",
        ],
        "variant_names": [
            "find_added_via_deviation",
            "find_removed_via_deviation",
            "find_replacement_diff",
            "find_count_via_deviation",
            "sum_of_deviations_zero",
        ],
    },
    5053: {
        "id": 5053,
        "name": "weighted_average",
        "description": "Combine averages across multiple groups with unequal weights or determine group weights.",
        "variants": [
            "two_groups_find_combined",
            "find_ratio_of_counts",
            "three_groups_find_combined",
            "find_missing_group_average",
            "weighted_percentage_marks",
        ],
        "variant_names": [
            "two_groups_find_combined",
            "find_ratio_of_counts",
            "three_groups_find_combined",
            "find_missing_group_average",
            "weighted_percentage_marks",
        ],
    },
    5054: {
        "id": 5054,
        "name": "weighted_average_intuition",
        "description": "Leverage visual and teeter-totter intuition to quickly eliminate choices in weighted average problems.",
        "variants": [
            "pulled_towards_larger_group",
            "equal_sizes_vs_unequal",
            "teeter_totter_leverage",
            "quick_elimination_bounds",
            "weighted_average_ds_style",
        ],
        "variant_names": [
            "pulled_towards_larger_group",
            "equal_sizes_vs_unequal",
            "teeter_totter_leverage",
            "quick_elimination_bounds",
            "weighted_average_ds_style",
        ],
    },
    5055: {
        "id": 5055,
        "name": "gmat_mixed_questions",
        "description": "Multi-topic integration combining ratios, averages, percentages, and profit/loss.",
        "variants": [
            "ratio_and_percentage",
            "ratio_and_average",
            "percentage_and_profit_loss",
            "fraction_and_percentage_shift",
            "ratio_average_percentage_trio",
        ],
        "variant_names": [
            "ratio_and_percentage",
            "ratio_and_average",
            "percentage_and_profit_loss",
            "fraction_and_percentage_shift",
            "ratio_average_percentage_trio",
        ],
    },
}

# Add string and ID aliases to DAY4_PATTERNS_METADATA for flexibility
for _pid in list(DAY4_PATTERNS_METADATA.keys()):
    _data = DAY4_PATTERNS_METADATA[_pid]
    DAY4_PATTERNS_METADATA[str(_pid)] = _data
    DAY4_PATTERNS_METADATA[_data["name"]] = _data


DAY4_GENERATORS: Dict[Any, Any] = {
    # Keyed by pattern name
    "ratio_basics": generate_ratio_basics,
    "ratio_with_total": generate_ratio_with_total,
    "ratio_one_value_known": generate_ratio_one_value_known,
    "ratio_changes": generate_ratio_changes,
    "ratio_variables_x_method": generate_ratio_variables_x_method,
    "proportion": generate_proportion,
    "direct_proportion": generate_direct_proportion,
    "inverse_proportion": generate_inverse_proportion,
    "average_basics": generate_average_basics,
    "missing_number_average": generate_missing_number_average,
    "adding_number_to_average": generate_adding_number_to_average,
    "removing_number_from_average": generate_removing_number_from_average,
    "average_change_shortcut": generate_average_change_shortcut,
    "weighted_average": generate_weighted_average,
    "weighted_average_intuition": generate_weighted_average_intuition,
    "gmat_mixed_questions": generate_gmat_mixed_questions,
    # Keyed by integer pattern ID
    5040: generate_ratio_basics,
    5041: generate_ratio_with_total,
    5042: generate_ratio_one_value_known,
    5043: generate_ratio_changes,
    5044: generate_ratio_variables_x_method,
    5045: generate_proportion,
    5046: generate_direct_proportion,
    5047: generate_inverse_proportion,
    5048: generate_average_basics,
    5049: generate_missing_number_average,
    5050: generate_adding_number_to_average,
    5051: generate_removing_number_from_average,
    5052: generate_average_change_shortcut,
    5053: generate_weighted_average,
    5054: generate_weighted_average_intuition,
    5055: generate_gmat_mixed_questions,
    # Keyed by string pattern ID
    "5040": generate_ratio_basics,
    "5041": generate_ratio_with_total,
    "5042": generate_ratio_one_value_known,
    "5043": generate_ratio_changes,
    "5044": generate_ratio_variables_x_method,
    "5045": generate_proportion,
    "5046": generate_direct_proportion,
    "5047": generate_inverse_proportion,
    "5048": generate_average_basics,
    "5049": generate_missing_number_average,
    "5050": generate_adding_number_to_average,
    "5051": generate_removing_number_from_average,
    "5052": generate_average_change_shortcut,
    "5053": generate_weighted_average,
    "5054": generate_weighted_average_intuition,
    "5055": generate_gmat_mixed_questions,
}


class RatiosAndAveragesMixin:
    """Mixin exposing Ratios, Proportion and Averages generators."""
    generate_ratio_basics = staticmethod(generate_ratio_basics)
    generate_ratio_with_total = staticmethod(generate_ratio_with_total)
    generate_ratio_one_value_known = staticmethod(generate_ratio_one_value_known)
    generate_ratio_changes = staticmethod(generate_ratio_changes)
    generate_ratio_variables_x_method = staticmethod(generate_ratio_variables_x_method)
    generate_proportion = staticmethod(generate_proportion)
    generate_direct_proportion = staticmethod(generate_direct_proportion)
    generate_inverse_proportion = staticmethod(generate_inverse_proportion)
    generate_average_basics = staticmethod(generate_average_basics)
    generate_missing_number_average = staticmethod(generate_missing_number_average)
    generate_adding_number_to_average = staticmethod(generate_adding_number_to_average)
    generate_removing_number_from_average = staticmethod(generate_removing_number_from_average)
    generate_average_change_shortcut = staticmethod(generate_average_change_shortcut)
    generate_weighted_average = staticmethod(generate_weighted_average)
    generate_weighted_average_intuition = staticmethod(generate_weighted_average_intuition)
    generate_gmat_mixed_questions = staticmethod(generate_gmat_mixed_questions)


__all__ = [
    "DAY4_GENERATORS",
    "DAY4_PATTERNS_METADATA",
    "RatiosAndAveragesMixin",
    "generate_ratio_basics",
    "generate_ratio_with_total",
    "generate_ratio_one_value_known",
    "generate_ratio_changes",
    "generate_ratio_variables_x_method",
    "generate_proportion",
    "generate_direct_proportion",
    "generate_inverse_proportion",
    "generate_average_basics",
    "generate_missing_number_average",
    "generate_adding_number_to_average",
    "generate_removing_number_from_average",
    "generate_average_change_shortcut",
    "generate_weighted_average",
    "generate_weighted_average_intuition",
    "generate_gmat_mixed_questions",
]
