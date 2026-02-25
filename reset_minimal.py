from database.db_manager import db

def reset_and_seed_minimal():
    print("--- 🗑️ Resetting Database (Minimal Syllabus) ---")
    
    # 1. Clear old data (Maintain categories but clear topics/patterns)
    # user_added_patterns and user_progress must be cleared first due to FKs
    db.execute_query("DELETE FROM user_progress")
    db.execute_query("DELETE FROM user_added_patterns")
    db.execute_query("DELETE FROM questions")
    db.execute_query("DELETE FROM patterns")
    db.execute_query("DELETE FROM topics")
    
    # 2. Re-seed Categories (Quant, Reasoning, Data Insights)
    # These should already exist via schema.sql but let's be 100% sure
    db.execute_query("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING", ("Quant",))
    db.execute_query("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING", ("Reasoning",))
    db.execute_query("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING", ("Data Insights",))
    
    res = db.execute_query("SELECT id FROM categories WHERE name = %s", ("Quant",))
    quant_id = res[0]['id']
    
    # 3. Add Only "Percentages" Topic
    db.execute_query("INSERT INTO topics (category_id, name) VALUES (%s, %s)", (quant_id, "Percentages"))
    res = db.execute_query("SELECT id FROM topics WHERE name = %s", ("Percentages",))
    topic_id = res[0]['id']
    
    # 4. Add the 4 Foundational Patterns
    patterns = [
        ("Mix fraction", "Convert improper fractions to mixed fractions and vice versa."),
        ("Fraction subtraction", "Subtract fractions with common and uncommon denominators."),
        ("Per to fraction and vice versa", "Convert decimals and percentages to simplified fractions."),
        ("basic fraction to per", "Memorize common GMAT benchmark conversions (1/2 to 1/40).")
    ]
    
    for name, desc in patterns:
        print(f"Adding foundational pattern: {name}")
        db.add_pattern(topic_id, name, desc, 2)
        
    print("\n✅ Database Reset Complete! Only foundational patterns are now active.")

if __name__ == "__main__":
    reset_and_seed_minimal()
