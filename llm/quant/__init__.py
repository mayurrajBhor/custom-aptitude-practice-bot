"""Unified Quantitative Aptitude Package (Category 1: Quant).

Topics:
- vedic_math (Patterns 3001-3016)
- percentages (Patterns 1001-1007)
- number_sense (Patterns 5001-5009)
- fractions_and_decimals (Patterns 5010-5024)
- commercial_math (Patterns 5025-5039)
- ratios_and_averages (Patterns 5040-5055)
"""

from typing import Any, Callable, Dict, List, Optional, Union

from .commercial_math import CommercialMathMixin, DAY3_GENERATORS, DAY3_PATTERNS_METADATA
from .fractions_and_decimals import FractionsAndDecimalsMixin, DAY2_GENERATORS, DAY2_PATTERNS_METADATA
from .number_sense import NumberSenseMixin, DAY1_GENERATORS, DAY1_PATTERNS_METADATA
from .percentages import PercentagesMixin
from .ratios_and_averages import RatiosAndAveragesMixin, DAY4_GENERATORS, DAY4_PATTERNS_METADATA
from .vedic_math import VedicMathMixin


class QuantMixin(
    PercentagesMixin,
    VedicMathMixin,
    NumberSenseMixin,
    FractionsAndDecimalsMixin,
    CommercialMathMixin,
    RatiosAndAveragesMixin,
):
    """Unified Quant mixin aggregating all 6 quantitative topics."""
    pass


def _extract_unique_metadata(meta_dict: Dict[Any, Any], topic_id: int, topic_name: str) -> List[Dict[str, Any]]:
    items = []
    seen_ids = set()
    for k, v in meta_dict.items():
        if isinstance(k, int) and k not in seen_ids:
            seen_ids.add(k)
            item = dict(v)
            item["topic_id"] = topic_id
            item["topic_name"] = topic_name
            items.append(item)
    return sorted(items, key=lambda x: x["id"])


DAY1_LIST = _extract_unique_metadata(DAY1_PATTERNS_METADATA, 501, "Day 1: Number Sense & Basic Arithmetic")
DAY2_LIST = _extract_unique_metadata(DAY2_PATTERNS_METADATA, 502, "Day 2: Fractions & Decimals")
DAY3_LIST = _extract_unique_metadata(DAY3_PATTERNS_METADATA, 503, "Day 3: Percentages & Commercial Math")
DAY4_LIST = _extract_unique_metadata(DAY4_PATTERNS_METADATA, 504, "Day 4: Ratios, Proportion & Averages")

ALL_GMAT_PATTERNS_METADATA = DAY1_LIST + DAY2_LIST + DAY3_LIST + DAY4_LIST

ALL_GMAT_GENERATORS: Dict[Union[int, str], Callable[..., Dict[str, Any]]] = {}
ALL_GMAT_GENERATORS.update(DAY1_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY2_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY3_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY4_GENERATORS)

PATTERNS_BY_ID = {p["id"]: p for p in ALL_GMAT_PATTERNS_METADATA}
PATTERNS_BY_NAME = {p["name"].lower(): p for p in ALL_GMAT_PATTERNS_METADATA}
for p in ALL_GMAT_PATTERNS_METADATA:
    if p.get("title"):
        PATTERNS_BY_NAME[p["title"].lower()] = p

GMAT_HYBRID_SUBTYPES: Dict[str, List[str]] = {}
for p in ALL_GMAT_PATTERNS_METADATA:
    code = p.get("code") or p["name"]
    variants = p.get("variants") or p.get("variant_names") or []
    GMAT_HYBRID_SUBTYPES[code] = variants
    GMAT_HYBRID_SUBTYPES[p["name"]] = variants
    if p.get("title"):
        GMAT_HYBRID_SUBTYPES[p["title"]] = variants


def get_gmat_generator(key: Union[int, str]) -> Optional[Callable[..., Dict[str, Any]]]:
    if key in ALL_GMAT_GENERATORS:
        return ALL_GMAT_GENERATORS[key]
    if isinstance(key, str):
        cleaned = key.strip().lower()
        if cleaned in ALL_GMAT_GENERATORS:
            return ALL_GMAT_GENERATORS[cleaned]
        if cleaned in PATTERNS_BY_NAME:
            pat_id = PATTERNS_BY_NAME[cleaned]["id"]
            return ALL_GMAT_GENERATORS.get(pat_id)
        if cleaned.isdigit():
            return ALL_GMAT_GENERATORS.get(int(cleaned))
    return None


def is_gmat_pattern_id(pattern_id: Any) -> bool:
    try:
        return int(pattern_id) in PATTERNS_BY_ID
    except (TypeError, ValueError):
        return False


def get_gmat_pattern_metadata(pattern_id: int) -> Optional[Dict[str, Any]]:
    return PATTERNS_BY_ID.get(pattern_id)


__all__ = [
    "QuantMixin",
    "PercentagesMixin",
    "VedicMathMixin",
    "NumberSenseMixin",
    "FractionsAndDecimalsMixin",
    "CommercialMathMixin",
    "RatiosAndAveragesMixin",
    "DAY1_LIST",
    "DAY2_LIST",
    "DAY3_LIST",
    "DAY4_LIST",
    "ALL_GMAT_PATTERNS_METADATA",
    "ALL_GMAT_GENERATORS",
    "PATTERNS_BY_ID",
    "PATTERNS_BY_NAME",
    "GMAT_HYBRID_SUBTYPES",
    "get_gmat_generator",
    "is_gmat_pattern_id",
    "get_gmat_pattern_metadata",
]
