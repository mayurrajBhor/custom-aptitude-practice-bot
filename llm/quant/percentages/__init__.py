from .fraction_foundations import FractionFoundationsMixin
from .core_percentage_equations import CorePercentageEquationsMixin
from .percentage_calculation_tricks import PercentageCalculationTricksMixin
from .applied_percentage_word_problems import AppliedPercentageWordProblemsMixin
from .mixtures_alligation_shifts import MixturesAlligationShiftsMixin
from .income_savings_exam import IncomeSavingsExamMixin
from .successive_changes_discounts import SuccessiveChangesDiscountsMixin


class PercentagesMixin(
    FractionFoundationsMixin,
    CorePercentageEquationsMixin,
    PercentageCalculationTricksMixin,
    AppliedPercentageWordProblemsMixin,
    MixturesAlligationShiftsMixin,
    IncomeSavingsExamMixin,
    SuccessiveChangesDiscountsMixin,
):
    """Combined mixin for all Percentages patterns (1001-1007)."""
    pass
