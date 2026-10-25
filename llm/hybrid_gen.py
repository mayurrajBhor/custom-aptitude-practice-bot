"""Unified Hybrid Question Generator composed from modular category packages.

Structure:
    llm/quant/percentages/     → 7 catalog patterns (1001-1007), 19 methods
    llm/quant/vedic_math/      → 16 catalog patterns (3001-3016), 16 methods
    llm/logical_reasoning/direction_and_distance/ → 16 catalog patterns (2001-2016)
    llm/di/                    → placeholder for Data Interpretation

All methods remain accessible via hybrid_generator.generate_*() for
backward compatibility with generator.py dispatch.
"""

from llm.common.base import BaseGenerator
from llm.quant import QuantMixin
from llm.logical_reasoning import LogicalReasoningMixin
from llm.di import DIMixin


class HybridGenerator(BaseGenerator, QuantMixin, LogicalReasoningMixin, DIMixin):
    """Unified hybrid question generator backward-compatible with all existing code."""
    pass


hybrid_generator = HybridGenerator()

__all__ = ["BaseGenerator", "HybridGenerator", "hybrid_generator"]
