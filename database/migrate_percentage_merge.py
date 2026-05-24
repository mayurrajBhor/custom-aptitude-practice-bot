import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database.db_manager import db


MERGED_PERCENTAGE_PATTERNS = [
    (
        "Fraction, Decimal and Percent Foundations",
        "Merged drills for mixed fractions, fraction subtraction, percent/fraction conversion, benchmark fractions, and fraction-to-decimal conversion.",
    ),
    (
        "Core Percentage Equations",
        "Merged drills for finding original values, percentage equations, ratios, multi-variable equalities, and third-anchor constraints.",
    ),
    (
        "Percentage Calculation Tricks",
        "Merged drills for swap property, decomposition, base comparisons, chained bases, product constancy, work/productivity, scaling, and error multipliers.",
    ),
    (
        "Applied Percentage Word Problems",
        "Merged application set covering populations, test scores, fraction shifts, nested comparisons, ratio equalization, weights, donations, and fractional populations.",
    ),
    (
        "Mixtures, Alligation and Shifts",
        "Merged mixture and shift applications, including alligation, population splits, value overlaps, and nested percentage shifts.",
    ),
    (
        "Income, Savings and Exam Aggregates",
        "Merged drills for income-expenditure-saving, pass/fail aggregates, weighted averages, marks, thresholds, and exam scoring.",
    ),
    (
        "Successive Changes and Discounts",
        "Merged drills for successive percentage increases/decreases, equivalent single changes, marked price, selling price, and successive discounts.",
    ),
]

LEGACY_PERCENTAGE_NAMES = [
    "Mix fraction",
    "Fraction subtraction",
    "Per to fraction and vice versa",
    "basic fraction to per",
    "find original number",
    "fraction to decimal and vice versa",
    "swap of percentage",
    "breakdown percentage",
    "percentage equations and ratios",
    "base comparisons and successive chains",
    "applied scenarios and complex calculations",
    "alligation and shift applications",
    "percentage comparisons",
    "percentage calculations",
    "income expenditure saving",
    "pass fail aggregates",
    "examination scoring",
    "successive percentage changes",
    "successive discount",
    "successive discounts",
    "successive changes",
]

LEGACY_TO_MERGED = {
    "mix fraction": "Fraction, Decimal and Percent Foundations",
    "fraction subtraction": "Fraction, Decimal and Percent Foundations",
    "per to fraction and vice versa": "Fraction, Decimal and Percent Foundations",
    "basic fraction to per": "Fraction, Decimal and Percent Foundations",
    "fraction to decimal": "Fraction, Decimal and Percent Foundations",
    "fraction to decimal and vice versa": "Fraction, Decimal and Percent Foundations",
    "find original number": "Core Percentage Equations",
    "percentage equations and ratios": "Core Percentage Equations",
    "swap of percentage": "Percentage Calculation Tricks",
    "breakdown percentage": "Percentage Calculation Tricks",
    "base comparisons and successive chains": "Percentage Calculation Tricks",
    "percentage calculations": "Percentage Calculation Tricks",
    "applied scenarios and complex calculations": "Applied Percentage Word Problems",
    "percentage comparisons": "Applied Percentage Word Problems",
    "alligation and shift applications": "Mixtures, Alligation and Shifts",
    "income expenditure saving": "Income, Savings and Exam Aggregates",
    "pass fail aggregates": "Income, Savings and Exam Aggregates",
    "examination scoring": "Income, Savings and Exam Aggregates",
    "successive percentage changes": "Successive Changes and Discounts",
    "successive discount": "Successive Changes and Discounts",
    "successive discounts": "Successive Changes and Discounts",
    "successive changes": "Successive Changes and Discounts",
}


def first_id(query, params):
    rows = db.execute_query(query, params)
    return rows[0]["id"] if rows else None


def merge_pattern_records(source_pattern_id, target_pattern_id):
    if source_pattern_id == target_pattern_id:
        return

    db.execute_query(
        "UPDATE questions SET pattern_id = %s WHERE pattern_id = %s",
        (target_pattern_id, source_pattern_id),
    )
    db.execute_query(
        "UPDATE question_attempts SET pattern_id = %s WHERE pattern_id = %s",
        (target_pattern_id, source_pattern_id),
    )
    db.execute_query(
        """
        UPDATE user_progress up
        SET pattern_id = %s
        WHERE pattern_id = %s
        AND NOT EXISTS (
            SELECT 1 FROM user_progress existing
            WHERE existing.user_id = up.user_id
            AND existing.pattern_id = %s
        )
        """,
        (target_pattern_id, source_pattern_id, target_pattern_id),
    )
    db.execute_query(
        "DELETE FROM user_progress WHERE pattern_id = %s",
        (source_pattern_id,),
    )
    db.execute_query(
        """
        UPDATE user_added_patterns uap
        SET pattern_id = %s
        WHERE pattern_id = %s
        AND NOT EXISTS (
            SELECT 1 FROM user_added_patterns existing
            WHERE existing.user_id = uap.user_id
            AND existing.pattern_id = %s
        )
        """,
        (target_pattern_id, source_pattern_id, target_pattern_id),
    )
    db.execute_query(
        "DELETE FROM user_added_patterns WHERE pattern_id = %s",
        (source_pattern_id,),
    )
    db.execute_query("DELETE FROM patterns WHERE id = %s", (source_pattern_id,))


def migrate_percentage_merge():
    db.init_db()

    quant_id = first_id("SELECT id FROM categories WHERE lower(name) = %s", ("quant",))
    if not quant_id:
        raise RuntimeError("Quant category not found. Run database/seed_data.py first.")

    db.execute_query(
        """
        INSERT INTO topics (category_id, name)
        VALUES (%s, %s)
        ON CONFLICT (category_id, name) DO NOTHING
        """,
        (quant_id, "Percentages"),
    )
    percentages_topic_id = first_id(
        "SELECT id FROM topics WHERE category_id = %s AND lower(name) = %s",
        (quant_id, "percentages"),
    )
    if not percentages_topic_id:
        raise RuntimeError("Percentages topic could not be created.")

    for name, description in MERGED_PERCENTAGE_PATTERNS:
        db.add_pattern(percentages_topic_id, name, description, 2)

    legacy_names = [name.lower() for name in LEGACY_PERCENTAGE_NAMES]

    db.execute_query(
        """
        UPDATE patterns
        SET is_unlocked = FALSE
        WHERE topic_id = %s AND lower(name) = ANY(%s)
        """,
        (percentages_topic_id, legacy_names),
    )

    db.execute_query(
        """
        UPDATE patterns p
        SET is_unlocked = FALSE
        FROM topics t
        WHERE p.topic_id = t.id
        AND t.category_id = %s
        AND t.id <> %s
        AND lower(t.name) = ANY(%s)
        """,
        (quant_id, percentages_topic_id, legacy_names),
    )

    legacy_topics = db.execute_query(
        """
        SELECT id, name
        FROM topics
        WHERE category_id = %s
        AND id <> %s
        AND lower(name) = ANY(%s)
        ORDER BY id
        """,
        (quant_id, percentages_topic_id, legacy_names),
    )

    for topic in legacy_topics or []:
        patterns = db.execute_query(
            "SELECT * FROM patterns WHERE topic_id = %s ORDER BY id",
            (topic["id"],),
        )

        for pattern in patterns or []:
            existing = db.execute_query(
                "SELECT id FROM patterns WHERE topic_id = %s AND name = %s",
                (percentages_topic_id, pattern["name"]),
            )

            if existing:
                target_pattern_id = existing[0]["id"]
                old_pattern_id = pattern["id"]
                merge_pattern_records(old_pattern_id, target_pattern_id)
            else:
                db.execute_query(
                    """
                    UPDATE patterns
                    SET topic_id = %s, is_unlocked = FALSE
                    WHERE id = %s
                    """,
                    (percentages_topic_id, pattern["id"]),
                )

        db.execute_query("DELETE FROM topics WHERE id = %s", (topic["id"],))

    target_pattern_ids = {}
    for target_name in set(LEGACY_TO_MERGED.values()):
        target_id = first_id(
            "SELECT id FROM patterns WHERE topic_id = %s AND name = %s",
            (percentages_topic_id, target_name),
        )
        if not target_id:
            raise RuntimeError(f"Merged target pattern not found: {target_name}")
        target_pattern_ids[target_name] = target_id

    legacy_patterns = db.execute_query(
        """
        SELECT id, name
        FROM patterns
        WHERE topic_id = %s AND lower(name) = ANY(%s)
        ORDER BY id
        """,
        (percentages_topic_id, list(LEGACY_TO_MERGED.keys())),
    )

    for pattern in legacy_patterns or []:
        target_name = LEGACY_TO_MERGED[pattern["name"].lower()]
        merge_pattern_records(pattern["id"], target_pattern_ids[target_name])

    visible_quant_topics = db.execute_query(
        """
        SELECT DISTINCT t.name
        FROM topics t
        JOIN patterns p ON p.topic_id = t.id
        WHERE t.category_id = %s AND p.is_unlocked = TRUE
        ORDER BY t.name
        """,
        (quant_id,),
    )
    visible_percentage_patterns = db.execute_query(
        """
        SELECT name
        FROM patterns
        WHERE topic_id = %s AND is_unlocked = TRUE
        ORDER BY id
        """,
        (percentages_topic_id,),
    )
    raw_percentage_patterns = db.execute_query(
        """
        SELECT name
        FROM patterns
        WHERE topic_id = %s
        ORDER BY id
        """,
        (percentages_topic_id,),
    )
    raw_quant_topics = db.execute_query(
        """
        SELECT name
        FROM topics
        WHERE category_id = %s
        ORDER BY id
        """,
        (quant_id,),
    )

    print("Visible Quant topics:")
    for row in visible_quant_topics or []:
        print(f"- {row['name']}")

    print("\nRaw Quant topics:")
    for row in raw_quant_topics or []:
        print(f"- {row['name']}")

    print("\nVisible Percentages patterns:")
    for row in visible_percentage_patterns or []:
        print(f"- {row['name']}")

    print("\nRaw Percentages patterns:")
    for row in raw_percentage_patterns or []:
        print(f"- {row['name']}")


if __name__ == "__main__":
    migrate_percentage_merge()
