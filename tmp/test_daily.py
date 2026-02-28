import sys, os
sys.path.append('.')
from database.db_manager import db
user_id = 123456  # test user
print('Syncing...')
db.sync_9_day_cycle(user_id)
new = db.get_new_patterns_in_cycle(user_id)
print('New patterns count:', len(new) if new else 0)
srs = db.get_srs_due_patterns(user_id)
print('SRS patterns count:', len(srs) if srs else 0)
unpr = db.get_unpracticed_patterns(user_id)
print('Unpracticed count:', len(unpr) if unpr else 0)
