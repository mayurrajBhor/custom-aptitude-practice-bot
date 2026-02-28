import os
import json
import psycopg2
import logging
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn_url = os.getenv("DATABASE_URL")
        self.conn = None

    def get_connection(self):
        # Check if connection exists and is alive
        should_reconnect = False
        if self.conn is None:
            should_reconnect = True
        else:
            try:
                # For Postgres, poll the connection to see if it's still alive
                if self.conn.closed != 0:
                    should_reconnect = True
                else:
                    self.conn.poll()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                should_reconnect = True

        if should_reconnect:
            logging.info("Re-establishing database connection...")
            try:
                self.conn = psycopg2.connect(self.conn_url, cursor_factory=RealDictCursor)
                with self.conn.cursor() as cur:
                    cur.execute("CREATE SCHEMA IF NOT EXISTS aptitude_practice")
                    cur.execute("SET search_path TO aptitude_practice, public")
                    self.conn.commit()
            except Exception as e:
                logging.error(f"Failed to connect to Postgres: {e}")
                self.conn = None
        return self.conn

    def execute_query(self, query, params=None, retries=1):
        for attempt in range(retries + 1):
            conn = self.get_connection()
            if not conn:
                return None
                
            try:
                cur = conn.cursor()
                cur.execute(query, params)
                conn.commit()
                if cur.description:
                    return cur.fetchall()
                return True # Success for non-SELECT queries
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                logging.error(f"Connection lost, retrying ({attempt+1}/{retries}): {e}")
                self.conn = None # Force reconnection on next get_connection()
                if attempt == retries:
                    return None
            except Exception as e:
                logging.error(f"Database error executing query: {e}\nQuery: {query}")
                if conn:
                    try:
                        conn.rollback()
                    except (psycopg2.InterfaceError, psycopg2.InternalError):
                        pass
                return None
        return None

    def init_db(self):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()
            
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            conn.commit()

    def get_user(self, user_id):
        return self.execute_query("SELECT * FROM users WHERE user_id = %s", (user_id,))

    def register_user(self, user_id, username, first_name, last_name):
        query = """
        INSERT INTO users (user_id, username, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
        """
        return self.execute_query(query, (user_id, username, first_name, last_name)) is not None

    def get_categories(self):
        return self.execute_query("SELECT * FROM categories")

    def get_topics(self, category_id):
        return self.execute_query("SELECT * FROM topics WHERE category_id = %s", (category_id,))

    def get_patterns(self, topic_id):
        return self.execute_query("SELECT * FROM patterns WHERE topic_id = %s", (topic_id,))

    def unlock_pattern(self, pattern_id):
        self.execute_query("UPDATE patterns SET is_unlocked = %s WHERE id = %s", (True, pattern_id))

    def save_question(self, pattern_id, question_text, options, correct_index, explanation, difficulty):
        query = """
        INSERT INTO questions (pattern_id, question_text, options, correct_option_index, explanation, difficulty)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        # psycopg2 handles dicts/lists for JSONB columns automatically
        self.execute_query(query, (pattern_id, question_text, options, correct_index, explanation, difficulty))

    def get_recent_questions(self, pattern_id, limit=50):
        query = "SELECT question_text FROM questions WHERE pattern_id = %s ORDER BY created_at DESC LIMIT %s"
        res = self.execute_query(query, (pattern_id, limit))
        return [r['question_text'] for r in res] if res else []

    def update_user_progress(self, user_id, pattern_id, is_correct, performance_score, time_taken=0.0):
        progress = self.execute_query("SELECT * FROM user_progress WHERE user_id = %s AND pattern_id = %s", (user_id, pattern_id))
        
        if not progress:
            res = self.execute_query("SELECT difficulty_level FROM patterns WHERE id = %s", (pattern_id,))
            base_diff = res[0]['difficulty_level'] if res else 2
            
            next_diff = base_diff
            if is_correct and time_taken < 90: next_diff = min(5, base_diff + 1)
            elif not is_correct: next_diff = max(1, base_diff - 1)

            query = """
            INSERT INTO user_progress (user_id, pattern_id, mastery_score, total_attempts, correct_attempts, last_practiced_at, avg_time_seconds, last_difficulty_level)
            VALUES (%s, %s, %s, 1, %s, CURRENT_TIMESTAMP, %s, %s)
            """
            self.execute_query(query, (user_id, pattern_id, 0.1 if is_correct else 0.0, 1 if is_correct else 0, time_taken, next_diff))
        else:
            p = progress[0]
            q = performance_score
            old_ef = p['easiness_factor']
            new_ef = max(1.3, old_ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
            
            new_avg_time = (p['avg_time_seconds'] * p['total_attempts'] + time_taken) / (p['total_attempts'] + 1)
            
            current_diff = p['last_difficulty_level'] or 1
            if is_correct:
                if time_taken < 90:
                    new_diff = min(5, current_diff + 1)
                else:
                    new_diff = current_diff
            else:
                new_diff = max(1, current_diff - 1)

            if is_correct:
                if p['total_attempts'] == 0:
                    new_interval = 1
                elif p['total_attempts'] == 1:
                    new_interval = 6
                else:
                    new_interval = round(p['srs_interval'] * new_ef)
            else:
                new_interval = 1
            
            query = """
            UPDATE user_progress SET
                total_attempts = total_attempts + 1,
                correct_attempts = correct_attempts + %s,
                last_practiced_at = CURRENT_TIMESTAMP,
                next_review_at = CURRENT_TIMESTAMP + (%s * interval '1 day'),
                srs_interval = %s,
                easiness_factor = %s,
                mastery_score = %s,
                avg_time_seconds = %s,
                last_difficulty_level = %s
            WHERE id = %s
            """
            new_mastery = min(1.0, (p['correct_attempts'] + (1 if is_correct else 0)) / (p['total_attempts'] + 1))
            params = (1 if is_correct else 0, new_interval, new_interval, new_ef, new_mastery, new_avg_time, new_diff, p['id'])
            
            self.execute_query(query, params)

    def get_current_difficulty(self, user_id, pattern_id):
        res = self.execute_query("SELECT last_difficulty_level FROM user_progress WHERE user_id = %s AND pattern_id = %s", (user_id, pattern_id))
        if res and res[0]['last_difficulty_level']:
            return res[0]['last_difficulty_level']
        
        res = self.execute_query("SELECT difficulty_level FROM patterns WHERE id = %s", (pattern_id,))
        return res[0]['difficulty_level'] if res else 2

    def add_pattern(self, topic_id, name, description, difficulty, user_id=None):
        query = """
        INSERT INTO patterns (topic_id, name, description, difficulty_level, is_unlocked)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        res = self.execute_query(query, (topic_id, name, description, difficulty, True))
        
        if res:
            pattern_id = res[0]['id']
        else:
            return None
        
        if user_id and pattern_id:
            self.record_pattern_addition(user_id, pattern_id)
        return pattern_id

    def record_pattern_addition(self, user_id, pattern_id):
        query = "INSERT INTO user_added_patterns (user_id, pattern_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        self.execute_query(query, (user_id, pattern_id))

    def get_new_patterns_in_cycle(self, user_id):
        """Patterns added in the last 9 days."""
        query = """
        SELECT p.*, t.name as topic_name, uap.added_at
        FROM user_added_patterns uap
        JOIN patterns p ON uap.pattern_id = p.id
        JOIN topics t ON p.topic_id = t.id
        WHERE uap.user_id = %s 
        AND uap.added_at >= CURRENT_TIMESTAMP - interval '9 days'
        """
        return self.execute_query(query, (user_id,))

    def get_srs_due_patterns(self, user_id):
        """Patterns due for SRS review."""
        query = """
        SELECT p.*, t.name as topic_name, up.mastery_score, up.avg_time_seconds
        FROM user_progress up
        JOIN patterns p ON up.pattern_id = p.id
        JOIN topics t ON p.topic_id = t.id
        WHERE up.user_id = %s AND up.next_review_at <= CURRENT_TIMESTAMP
        """
        return self.execute_query(query, (user_id,))

    def get_unpracticed_patterns(self, user_id):
        """Patterns that are unlocked but have no user progress yet."""
        query = """
        SELECT p.*, t.name as topic_name
        FROM patterns p
        JOIN topics t ON p.topic_id = t.id
        LEFT JOIN user_progress up ON p.id = up.pattern_id AND up.user_id = %s
        WHERE p.is_unlocked = TRUE AND up.id IS NULL
        """
        return self.execute_query(query, (user_id,))

db = DatabaseManager()
