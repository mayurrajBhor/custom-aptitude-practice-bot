import sys
sys.path.append('.')
from database.db_manager import db

# The stale patterns to delete
stale_patterns = [
    "Find original number",
    "Fraction to decimal",
    "Swap of percentage",
    "Breakdown percentage"
]

for p_name in stale_patterns:
    res = db.execute_query("SELECT id FROM patterns WHERE name = %s", (p_name,))
    if res:
        for r in res:
            pid = r['id']
            print(f"Deleting stale pattern: '{p_name}' (ID: {pid})")
            db.execute_query("DELETE FROM user_progress WHERE pattern_id = %s", (pid,))
            db.execute_query("DELETE FROM questions WHERE pattern_id = %s", (pid,))
            db.execute_query("DELETE FROM user_added_patterns WHERE pattern_id = %s", (pid,))
            db.execute_query("DELETE FROM patterns WHERE id = %s", (pid,))
            
print("Cleanup complete.")
