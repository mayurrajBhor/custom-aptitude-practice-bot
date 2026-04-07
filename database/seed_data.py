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
    
    quant_patterns = [
        ("Mix fraction", "Convert improper fractions to mixed fractions and vice versa."),
        ("Fraction subtraction", "Subtract fractions with common and uncommon denominators."),
        ("Per to fraction and vice versa", "Convert decimals and percentages to simplified fractions."),
        ("basic fraction to per", "Memorize common GMAT benchmark conversions (1/2 to 1/40)."),
        ("find original number", "Solve percentage equations added or subtracted from themselves."),
        ("fraction to decimal and vice versa", "Advanced benchmark conversions."),
        ("swap of percentage", "a% of b equals b% of a, and scaling tricks."),
        ("breakdown percentage", "Decomposition, shifting, and repeating decimals."),
        ("percentage equations and ratios", "Multi-variable percentage equality, ratio conversions, and third-anchor constraints."),
        ("base comparisons and successive chains", "Direct base comparisons, missing values, and successive percentage chains."),
        ("applied scenarios and complex calculations", "Word problems for populations, test scores, fraction shifts, and tricks."),
        ("alligation and shift applications", "Mixtures, population splits, value overlaps, and double-shift nested percentages."),
        ("percentage comparisons", "Nested variable chains, sum-based relativity, ratio equalization, weight fractions, donation differences, and fractional populations."),
        ("percentage calculations", "Product constancy, work & productivity, geometric scaling, error multipliers, salary remainders, property value chains, and spoiled subset problems."),
        ("income expenditure saving", "Successive scaling, constant equations, finding percentage changes and backtracking original values across Income = Expenditure + Savings."),
        ("pass fail aggregates", "Complex weighted averages, multi-object sizing, scaling productivity margins, and subset presence distributions."),
        ("examination scoring", "Max marks, pass/fail thresholds, sum-difference relationships, and ratio shifts in scoring."),
        ("successive percentage changes", "Calculating single equivalent change for multiple random percentage increases or decreases.")
    ]
    
    for name, desc in quant_patterns:
        db.add_pattern(topic_id, name, desc, 2)

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
