from .speed_addition import SpeedAdditionMixin
from .speed_subtraction import SpeedSubtractionMixin
from .mental_multiplication import MentalMultiplicationMixin
from .fast_division import FastDivisionMixin
from .tables_multiples import TablesMultiplesMixin
from .squares_roots import SquaresRootsMixin
from .cubes_roots import CubesRootsMixin
from .divisibility_rules import DivisibilityRulesMixin
from .approximation import ApproximationMixin
from .odd_even import OddEvenMixin
from .prime_composite import PrimeCompositeMixin
from .factors import FactorsMixin
from .multiples import MultiplesMixin
from .prime_factorization import PrimeFactorizationMixin
from .hcf_gcd import HcfGcdMixin
from .lcm import LcmMixin


class VedicMathMixin(
    SpeedAdditionMixin,
    SpeedSubtractionMixin,
    MentalMultiplicationMixin,
    FastDivisionMixin,
    TablesMultiplesMixin,
    SquaresRootsMixin,
    CubesRootsMixin,
    DivisibilityRulesMixin,
    ApproximationMixin,
    OddEvenMixin,
    PrimeCompositeMixin,
    FactorsMixin,
    MultiplesMixin,
    PrimeFactorizationMixin,
    HcfGcdMixin,
    LcmMixin,
):
    """Combined mixin for all Vedic Math patterns (3001-3016)."""
    pass
