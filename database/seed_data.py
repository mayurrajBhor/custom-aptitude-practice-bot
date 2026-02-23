from db_manager import db

def seed_gmat_data():
    # 1. Categories
    db.init_db() # Ensure tables exist
    
    # Categories are inserted via ON CONFLICT in schema.sql but let's be sure
    res = db.get_categories()
    cat_map = {row['name']: row['id'] for row in res}
    
    # 2. Topics and Patterns
    syllabus = {
        'Quant': {
            'Number Properties': [('Integers', 'Properties of integers, prime numbers, etc.')],
            'Percentages': [('Percent Change', 'Calculating percentage increases and decreases.')],
            'Profit & Loss': [('Cost/Price/Margin', 'Calculating markups and margins.')],
            'Ratios & Proportions': [('Division of Quantities', 'Splitting values based on ratios.')],
            'Algebra': [('Linear Equations', 'Single and double variable equations.')],
            'Geometry': [('Triangles & Circles', 'Area and perimeter formulas.')],
            'Work & Rate': [('Combined Work', 'Problems involving rates of multiple people.')],
        },
        'Reasoning': {
            'Critical Reasoning': [('Strengthen/Weaken', 'Evaluate arguments.')],
            'Sentence Correction': [('Grammar & Style', 'Subject-verb agreement and more.')],
        },
        'Data Insights': {
            'Data Sufficiency': [('Value DS', 'Determining sufficiency for values.')],
            'Graphics Interpretation': [('Trend Analysis', 'Reading data from charts.')],
        }
    }
    
    for cat_name, topics in syllabus.items():
        cat_id = cat_map[cat_name]
        for topic_name, patterns_list in topics.items():
            db.execute_query("INSERT INTO topics (category_id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING", (cat_id, topic_name))
            # Patterns removed as requested.

if __name__ == "__main__":
    seed_gmat_data()
    print("Database seeded successfully with initial GMAT syllabus.")
