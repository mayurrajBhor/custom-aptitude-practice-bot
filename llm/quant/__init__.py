from .percentages import PercentagesMixin
from .vedic_math import VedicMathMixin


class QuantMixin(PercentagesMixin, VedicMathMixin):
    """Aggregated Quant mixin covering Percentages and Vedic Math."""
    pass
