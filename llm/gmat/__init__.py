from typing import Any, Callable, Dict, List, Optional, Union

from llm.gmat.day1_arithmetic import DAY1_GENERATORS, DAY1_PATTERNS_METADATA
from llm.gmat.day2_fractions import DAY2_GENERATORS, DAY2_PATTERNS_METADATA
from llm.gmat.day3_percentages import DAY3_GENERATORS, DAY3_PATTERNS_METADATA
from llm.gmat.day4_ratios_averages import DAY4_GENERATORS, DAY4_PATTERNS_METADATA
from llm.gmat.mistakes import MISTAKE_CATEGORIES, classify_mistake

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

# Master list of all 55 patterns
ALL_GMAT_PATTERNS_METADATA = DAY1_LIST + DAY2_LIST + DAY3_LIST + DAY4_LIST

# Merge all generators
ALL_GMAT_GENERATORS: Dict[Union[int, str], Callable[..., Dict[str, Any]]] = {}
ALL_GMAT_GENERATORS.update(DAY1_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY2_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY3_GENERATORS)
ALL_GMAT_GENERATORS.update(DAY4_GENERATORS)

# Map by canonical integer ID
PATTERNS_BY_ID = {p["id"]: p for p in ALL_GMAT_PATTERNS_METADATA}
# Map by pattern name lower
PATTERNS_BY_NAME = {p["name"].lower(): p for p in ALL_GMAT_PATTERNS_METADATA}
# Also map by title lower if title exists
for p in ALL_GMAT_PATTERNS_METADATA:
    if p.get("title"):
        PATTERNS_BY_NAME[p["title"].lower()] = p

# Subtype dictionary mapping for QuestionGenerator.HYBRID_SUBTYPES
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
        # Check by name
        if cleaned in PATTERNS_BY_NAME:
            pat_id = PATTERNS_BY_NAME[cleaned]["id"]
            return ALL_GMAT_GENERATORS.get(pat_id)
        # Check if digits
        if cleaned.isdigit():
            return ALL_GMAT_GENERATORS.get(int(cleaned))
    return None


def is_gmat_pattern_id(pattern_id: Any) -> bool:
    try:
        pid = int(pattern_id)
        return pid in PATTERNS_BY_ID
    except (TypeError, ValueError):
        return False


def get_gmat_pattern_metadata(pattern_id: int) -> Optional[Dict[str, Any]]:
    return PATTERNS_BY_ID.get(pattern_id)
