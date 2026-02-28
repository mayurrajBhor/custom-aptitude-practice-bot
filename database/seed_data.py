from database.db_manager import db

def seed_gmat_data():
    # 1. Categories
    db.init_db() # Ensure tables exist
    
    # Categories are inserted via ON CONFLICT in schema.sql but let's be sure
    res = db.get_categories()
    cat_map = {row['name']: row['id'] for row in res}
    
    # 2. Minimal Syllabus
    quant_id = cat_map['Quant']
    db.execute_query("INSERT INTO topics (category_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (quant_id, "Percentages"))
    
    res = db.execute_query("SELECT id FROM topics WHERE name = %s", ("Percentages",))
    topic_id = res[0]['id']
    
    patterns = [
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
        ("applied scenarios and complex calculations", "Word problems for populations, test scores, fraction shifts, and tricks.")
    ]
    
    for name, desc in patterns:
        db.add_pattern(topic_id, name, desc, 2)

if __name__ == "__main__":
    seed_gmat_data()
    print("Database seeded successfully with minimal FOUNDATIONAL syllabus.")
