from database.db_manager import db

def check_db():
    print("--- Topics ---")
    topics = db.execute_query("SELECT id, name FROM topics")
    if topics:
        for t in topics:
            print(f"Topic ID: {t['id']}, Name: {t['name']}")
    
    print("\n--- Patterns ---")
    patterns = db.execute_query("SELECT id, topic_id, name FROM patterns")
    if patterns:
        for p in patterns:
            print(f"Pattern ID: {p['id']}, Topic ID: {p['topic_id']}, Name: '{p['name']}'")
    else:
        print("No patterns found.")

if __name__ == "__main__":
    check_db()
