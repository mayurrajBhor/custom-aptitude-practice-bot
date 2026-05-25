from copy import deepcopy

from llm.generator import generator


PERCENTAGE_PATTERNS = [
    (
        1001,
        "Fraction, Decimal and Percent Foundations",
        "Merged drills for mixed fractions, fraction subtraction, percent/fraction conversion, benchmark fractions, and fraction-to-decimal conversion.",
    ),
    (
        1002,
        "Core Percentage Equations",
        "Merged drills for finding original values, percentage equations, ratios, multi-variable equalities, and third-anchor constraints.",
    ),
    (
        1003,
        "Percentage Calculation Tricks",
        "Merged drills for swap property, decomposition, base comparisons, chained bases, product constancy, work/productivity, scaling, and error multipliers.",
    ),
    (
        1004,
        "Applied Percentage Word Problems",
        "Merged application set covering populations, test scores, fraction shifts, nested comparisons, ratio equalization, weights, donations, and fractional populations.",
    ),
    (
        1005,
        "Mixtures, Alligation and Shifts",
        "Merged mixture and shift applications, including alligation, population splits, value overlaps, and nested percentage shifts.",
    ),
    (
        1006,
        "Income, Savings and Exam Aggregates",
        "Merged drills for income-expenditure-saving, pass/fail aggregates, weighted averages, marks, thresholds, and exam scoring.",
    ),
    (
        1007,
        "Successive Changes and Discounts",
        "Merged drills for successive percentage increases/decreases, equivalent single changes, marked price, selling price, and successive discounts.",
    ),
]

DIRECTION_PATTERNS = [
    (2001, "Clockwise and anti clockwise", "Questions involving angular turns in clockwise and anti-clockwise directions."),
    (2002, "Pythagoras theorem", "Shortest distance calculations using the Pythagorean theorem."),
    (2003, "Starting without direction", "Finding the initial direction given the final facing direction and a series of turns."),
    (2004, "Moving towards different direction", "Complex movements involving multiple turns and distance tracking."),
    (2005, "Interchange direction", "Hypothetical scenarios where directions are renamed, such as North becoming West."),
    (2006, "Find direction in respect to another", "Relative positioning of points or houses in a grid."),
    (2007, "Side movement", "Movement along the sides or diagonals of a square or rectangular field."),
    (2008, "Coded direction", "Directions represented by symbols and codes."),
    (2009, "Shadow based", "Finding directions based on the position of shadows at sunrise or sunset."),
    (2010, "Headstand", "Direction identification while in an inverted headstand position."),
    (2011, "Playing cards", "Seating arrangements and facing directions of partners in a card game."),
    (2012, "Direction of smoke", "Determining smoke direction based on train movement and wind flow."),
    (2013, "Based on turns", "Determining the sequence of turns needed to reach a specific destination."),
    (2014, "Only one direction given", "Navigating an intersection given one or more landmark directions."),
    (2015, "Seating arrangement", "Circular or linear seating relative to cardinal directions."),
    (2016, "Instructions based", "Following movement instructions to find the final position or direction."),
]

VEDIC_MATH_PATTERNS = [
    (
        3001,
        "Speed Addition and Complements",
        "Mental addition drills using left-to-right addition, complement pairs, missing addends, and near-base sums.",
    ),
    (
        3002,
        "Speed Subtraction and Complements",
        "Fast subtraction drills using borrowing shortcuts, all-from-9-last-from-10, near-base differences, and missing minuends.",
    ),
    (
        3003,
        "Mental Multiplication",
        "Vedic multiplication drills covering vertical-and-crosswise, near-base products, multiplying by 11, split multiplication, and 25/125 shortcuts.",
    ),
    (
        3004,
        "Fast Division and Remainders",
        "Speed division drills covering short division, remainders, division by 25 or 125, and dividend reconstruction.",
    ),
    (
        3005,
        "Tables and Multiples Mastery",
        "Table fluency drills for products, missing factors, next multiples, and factor splitting.",
    ),
    (
        3006,
        "Squares and Square Roots",
        "Square and square-root drills including ending-in-5 squares, near-base squares, two-digit squares, perfect roots, and integer square roots.",
    ),
    (
        3007,
        "Cubes and Cube Roots",
        "Cube and cube-root drills covering cube values, perfect cube roots, nearest cube roots, and unit digit patterns.",
    ),
    (
        3008,
        "Divisibility Rules",
        "Divisibility-rule drills for 3, 4, 8, 9, 11, and combined aptitude checks.",
    ),
    (
        3009,
        "Approximation and Number Sense",
        "Speed estimation drills using compatible numbers, rounded products, rounded division, and benchmark percentages.",
    ),
]


def _pattern(pattern_id, topic_id, topic_name, name, description, difficulty=2):
    variants = generator.get_hybrid_variants(name)
    return {
        "id": pattern_id,
        "topic_id": topic_id,
        "topic_name": topic_name,
        "name": name,
        "description": description,
        "difficulty": difficulty,
        "difficulty_level": difficulty,
        "variant_count": len(variants) if variants else 1,
        "source": "local",
    }


LOCAL_PATTERNS = {
    pattern_id: _pattern(pattern_id, 101, "Percentages", name, description)
    for pattern_id, name, description in PERCENTAGE_PATTERNS
}
LOCAL_PATTERNS.update(
    {
        pattern_id: _pattern(pattern_id, 201, "Direction and distance", name, description)
        for pattern_id, name, description in DIRECTION_PATTERNS
    }
)
LOCAL_PATTERNS.update(
    {
        pattern_id: _pattern(pattern_id, 102, "Vedic Math", name, description)
        for pattern_id, name, description in VEDIC_MATH_PATTERNS
    }
)


LOCAL_TOPICS = {
    101: {"id": 101, "category_id": 1, "name": "Percentages", "pattern_ids": [item[0] for item in PERCENTAGE_PATTERNS]},
    102: {"id": 102, "category_id": 1, "name": "Vedic Math", "pattern_ids": [item[0] for item in VEDIC_MATH_PATTERNS]},
    201: {
        "id": 201,
        "category_id": 2,
        "name": "Direction and distance",
        "pattern_ids": [item[0] for item in DIRECTION_PATTERNS],
    },
}

LOCAL_CATEGORIES = [
    {"id": 1, "name": "Quant", "topic_ids": [101, 102]},
    {"id": 2, "name": "Reasoning", "topic_ids": [201]},
]


def get_local_pattern(pattern_id):
    pattern = LOCAL_PATTERNS.get(pattern_id)
    return deepcopy(pattern) if pattern else None


def is_local_pattern_id(pattern_id):
    return pattern_id in LOCAL_PATTERNS


def get_local_catalog_payload():
    categories = []
    for category in LOCAL_CATEGORIES:
        topics = []
        for topic_id in category["topic_ids"]:
            topic = LOCAL_TOPICS[topic_id]
            patterns = [deepcopy(LOCAL_PATTERNS[pattern_id]) for pattern_id in topic["pattern_ids"]]
            variant_count = sum(pattern["variant_count"] for pattern in patterns)
            topics.append(
                {
                    "id": topic["id"],
                    "name": topic["name"],
                    "description": "",
                    "pattern_count": len(patterns),
                    "variant_count": variant_count,
                    "patterns": patterns,
                }
            )

        categories.append({"id": category["id"], "name": category["name"], "topics": topics})

    return categories
