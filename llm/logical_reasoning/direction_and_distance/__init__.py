from .clockwise_anticlockwise import ClockwiseAnticlockwiseMixin
from .pythagoras_theorem import PythagorasTheoremMixin
from .starting_without_direction import StartingWithoutDirectionMixin
from .moving_towards_direction import MovingTowardsDirectionMixin
from .interchange_direction import InterchangeDirectionMixin
from .find_direction_respect import FindDirectionRespectMixin
from .side_movement import SideMovementMixin
from .coded_direction import CodedDirectionMixin
from .shadow_based import ShadowBasedMixin
from .headstand import HeadstandMixin
from .playing_cards import PlayingCardsMixin
from .direction_of_smoke import DirectionOfSmokeMixin
from .based_on_turns import BasedOnTurnsMixin
from .one_direction_only import OneDirectionOnlyMixin
from .seating_arrangement import SeatingArrangementMixin
from .instructions_based import InstructionsBasedMixin


class DirectionDistanceMixin(
    ClockwiseAnticlockwiseMixin,
    PythagorasTheoremMixin,
    StartingWithoutDirectionMixin,
    MovingTowardsDirectionMixin,
    InterchangeDirectionMixin,
    FindDirectionRespectMixin,
    SideMovementMixin,
    CodedDirectionMixin,
    ShadowBasedMixin,
    HeadstandMixin,
    PlayingCardsMixin,
    DirectionOfSmokeMixin,
    BasedOnTurnsMixin,
    OneDirectionOnlyMixin,
    SeatingArrangementMixin,
    InstructionsBasedMixin,
):
    """Combined mixin for all Direction and Distance patterns (2001-2016)."""
    pass
