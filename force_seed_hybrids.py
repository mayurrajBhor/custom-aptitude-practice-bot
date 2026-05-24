from database.db_manager import db

def force_seed_hybrids():
    print("--- Force Seeding Hybrid Patterns ---")
    
    # 1. Get Topic ID for Percentages
    res = db.execute_query("SELECT id FROM topics WHERE name = %s", ("Percentages",))
    if not res:
        print("Error: Topic 'Percentages' not found.")
        return
    topic_id = res[0]['id']
    
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
        print(f"Adding pattern: {name}")
        # Using add_pattern method which handles RETURNING id and user_added_patterns if needed
        # We'll use a dummy user_id or None
        db.add_pattern(topic_id, name, desc, 2)
    
    print("Done! Patterns should now be visible.")

if __name__ == "__main__":
    force_seed_hybrids()
