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
        ("Mix fraction", "Conver improper fractions to mixed fractions and vice versa."),
        ("Fraction subtraction", "Subtract fractions with common and uncommon denominators."),
        ("Per to fraction and vice versa", "Convert decimals and percentages to simplified fractions."),
        ("basic fraction to per", "Memorize common GMAT benchmark conversions (1/2 to 1/40).")
    ]
    
    for name, desc in patterns:
        print(f"Adding pattern: {name}")
        # Using add_pattern method which handles RETURNING id and user_added_patterns if needed
        # We'll use a dummy user_id or None
        db.add_pattern(topic_id, name, desc, 2)
    
    print("Done! Patterns should now be visible.")

if __name__ == "__main__":
    force_seed_hybrids()
