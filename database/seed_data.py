from database.db_manager import db

def seed_gmat_data():
    # 1. Categories
    db.init_db() # Ensure tables exist
    
    # Categories are inserted via ON CONFLICT in schema.sql but let's be sure
    res = db.get_categories()
    cat_map = {row['name']: row['id'] for row in res}
    
    # 2. Minimal Syllabus
    # Quant - Percentages
    quant_id = cat_map['Quant']
    db.execute_query("INSERT INTO topics (category_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (quant_id, "Percentages"))
    
    res = db.execute_query("SELECT id FROM topics WHERE name = %s", ("Percentages",))
    topic_id = res[0]['id']
    
    legacy_percentage_patterns = [
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
    ]
    legacy_percentage_topics = legacy_percentage_patterns + [
        "Successive discount",
        "Successive discounts",
        "Successive changes",
        "Successive percentage changes",
    ]

    quant_patterns = [
        ("Fraction, Decimal and Percent Foundations", "Merged drills for mixed fractions, fraction subtraction, percent/fraction conversion, benchmark fractions, and fraction-to-decimal conversion."),
        ("Core Percentage Equations", "Merged drills for finding original values, percentage equations, ratios, multi-variable equalities, and third-anchor constraints."),
        ("Percentage Calculation Tricks", "Merged drills for swap property, decomposition, base comparisons, chained bases, product constancy, work/productivity, scaling, and error multipliers."),
        ("Applied Percentage Word Problems", "Merged application set covering populations, test scores, fraction shifts, nested comparisons, ratio equalization, weights, donations, and fractional populations."),
        ("Mixtures, Alligation and Shifts", "Merged mixture and shift applications, including alligation, population splits, value overlaps, and nested percentage shifts."),
        ("Income, Savings and Exam Aggregates", "Merged drills for income-expenditure-saving, pass/fail aggregates, weighted averages, marks, thresholds, and exam scoring."),
        ("Successive Changes and Discounts", "Merged drills for successive percentage increases/decreases, equivalent single changes, marked price, selling price, and successive discounts."),
    ]
    
    for name, desc in quant_patterns:
        db.add_pattern(topic_id, name, desc, 2)

    db.execute_query(
        """
        UPDATE patterns
        SET is_unlocked = FALSE
        WHERE topic_id = %s AND lower(name) = ANY(%s)
        """,
        (topic_id, [name.lower() for name in legacy_percentage_patterns])
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
        (quant_id, topic_id, [name.lower() for name in legacy_percentage_topics])
    )

    # Reasoning - Direction and Distance
    reasoning_id = cat_map['Reasoning']
    db.execute_query("INSERT INTO topics (category_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (reasoning_id, "Direction and distance"))
    
    res = db.execute_query("SELECT id FROM topics WHERE name = %s", ("Direction and distance",))
    dir_topic_id = res[0]['id']

    dir_patterns = [
        ("Clockwise and anti clockwise", "Questions involving angular turns in clockwise and anti-clockwise directions."),
        ("Pythagoras theorem", "Shortest distance calculations using the Pythagorean theorem."),
        ("Starting without direction", "Finding the initial direction given the final facing direction and a series of turns."),
        ("Moving towards different direction", "Complex movements involving multiple turns and distance tracking."),
        ("Interchange direction", "Hypothetical scenarios where directions are renamed (e.g., North becomes West)."),
        ("Find direction in respect to another", "Relative positioning of points or houses in a grid."),
        ("Side movement", "Movement along the sides or diagonals of a square/rectangular field."),
        ("Coded direction", "Directions represented by symbols (e.g., G#H means G is North of H)."),
        ("Shadow based", "Finding directions based on the position of shadows at sunrise or sunset."),
        ("Headstand", "Direction identification while in an inverted (headstand) position."),
        ("Playing cards", "Seating arrangements and facing directions of partners in a card game."),
        ("Direction of smoke", "Determining smoke direction based on train movement and wind flow."),
        ("Based on turns", "Determining the sequence of turns needed to reach a specific destination."),
        ("Only one direction given", "Navigating an intersection given the location of one or more landmarks."),
        ("Seating arrangement", "Circular or linear seating relative to cardinal directions."),
        ("Instructions based", "Following a specific set of movement instructions to find the final position.")
    ]

    for name, desc in dir_patterns:
        db.add_pattern(dir_topic_id, name, desc, 2)

if __name__ == "__main__":
    seed_gmat_data()
    print("Database seeded successfully with Foundational syllabus and Direction & Distance reasoning.")
