from database.db_manager import db

def reset_and_seed_minimal():
    print("--- 🗑️ Resetting Database (Minimal Syllabus) ---")
    
    # 1. Clear old data (Maintain categories but clear topics/patterns)
    # Attempt/question tables must be cleared first due to FKs into patterns.
    db.execute_query("DELETE FROM question_attempts")
    db.execute_query("DELETE FROM practice_sessions")
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
    
    # 4. Add the merged Percentages patterns
    patterns = [
        ("Fraction, Decimal and Percent Foundations", "Merged drills for mixed fractions, fraction subtraction, percent/fraction conversion, benchmark fractions, and fraction-to-decimal conversion."),
        ("Core Percentage Equations", "Merged drills for finding original values, percentage equations, ratios, multi-variable equalities, and third-anchor constraints."),
        ("Percentage Calculation Tricks", "Merged drills for swap property, decomposition, base comparisons, chained bases, product constancy, work/productivity, scaling, and error multipliers."),
        ("Applied Percentage Word Problems", "Merged application set covering populations, test scores, fraction shifts, nested comparisons, ratio equalization, weights, donations, and fractional populations."),
        ("Mixtures, Alligation and Shifts", "Merged mixture and shift applications, including alligation, population splits, value overlaps, and nested percentage shifts."),
        ("Income, Savings and Exam Aggregates", "Merged drills for income-expenditure-saving, pass/fail aggregates, weighted averages, marks, thresholds, and exam scoring."),
        ("Successive Changes and Discounts", "Merged drills for successive percentage increases/decreases, equivalent single changes, marked price, selling price, and successive discounts.")
    ]
    
    for name, desc in patterns:
        print(f"Adding merged pattern: {name}")
        db.add_pattern(topic_id, name, desc, 2)
        
    print("\n✅ Database Reset Complete! Only foundational patterns are now active.")

if __name__ == "__main__":
    reset_and_seed_minimal()
