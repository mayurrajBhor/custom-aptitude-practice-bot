import sys
sys.path.append('.')
from database.db_manager import db

patterns = db.execute_query("SELECT id, name FROM patterns ORDER BY id")
seen_names = set()
duplicates = []

for p in patterns:
    if p['name'] in seen_names:
        duplicates.append(p['id'])
    else:
        seen_names.add(p['name'])

if duplicates:
    print(f"Found {len(duplicates)} duplicate patterns. Deleting...")
    for pid in duplicates:
        print(f"Deleting pattern {pid}")
        # Need to delete dependent rows first if any
        db.execute_query("DELETE FROM user_progress WHERE pattern_id = %s", (pid,))
        db.execute_query("DELETE FROM questions WHERE pattern_id = %s", (pid,))
        db.execute_query("DELETE FROM user_added_patterns WHERE pattern_id = %s", (pid,))
        db.execute_query("DELETE FROM patterns WHERE id = %s", (pid,))
    print("Duplicates removed.")
else:
    print("No duplicates found.")
