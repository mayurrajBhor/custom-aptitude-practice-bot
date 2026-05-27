import os
import json
import hashlib
import psycopg2
import logging
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.conn_url = os.getenv("DATABASE_URL")
        self.conn = None
        self.driver = 'postgres'

    def get_connection(self):
        # Check if connection exists and is alive
        should_reconnect = False
        if self.conn is None:
            should_reconnect = True
        else:
            try:
                if self.conn.closed != 0:
                    should_reconnect = True
                else:
                    self.conn.poll()
            except (psycopg2.OperationalError, psycopg2.InterfaceError):
                should_reconnect = True

        if should_reconnect:
            logging.info("Attempting to connect to Supabase (Postgres)...")
            try:
                if not self.conn_url:
                    raise RuntimeError("DATABASE_URL is missing. Set it in .env or the deployment environment.")
                # Use a shorter timeout to fail fast if project is paused/invalid
                self.conn = psycopg2.connect(self.conn_url, cursor_factory=RealDictCursor, connect_timeout=10)
                with self.conn.cursor() as cur:
                    cur.execute("CREATE SCHEMA IF NOT EXISTS aptitude_practice")
                    cur.execute("SET search_path TO aptitude_practice, public")
                    self.conn.commit()
                logging.info("✅ Connected to Supabase.")
            except Exception as e:
                err_msg = str(e)
                if "Tenant or user not found" in err_msg:
                    logging.error("FATAL: Supabase Project ID is invalid or project is PAUSED. Please check your .env and Supabase dashboard.")
                else:
                    logging.error(f"Failed to connect to Supabase: {e}")
                self.conn = None
                raise e
        return self.conn

    def execute_query(self, query, params=None, retries=1):
        for attempt in range(retries + 1):
            try:
                conn = self.get_connection()
            except Exception as conn_err:
                if attempt == retries:
                    raise conn_err
                continue

            if not conn:
                if attempt == retries:
                    raise Exception("Failed to establish a database connection.")
                continue
                
            try:
                cur = conn.cursor()
                cur.execute("SET search_path TO aptitude_practice, public")
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                
                if cur.description:
                    results = cur.fetchall()
                else:
                    results = True
                conn.commit()
                return results
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                logging.error(f"Connection lost, retrying ({attempt+1}/{retries}): {e}")
                self.conn = None # Force reconnection
                if attempt == retries:
                    raise e
            except Exception as e:
                logging.error(f"Database error executing query: {e}\nQuery: {query}")
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                raise e
        return None

    def init_db(self):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()
            
        conn = self.get_connection()
        with conn.cursor() as cur:
            cur.execute(schema_sql)
            conn.commit()

    def ensure_engagement_schema(self):
        statements = [
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS question_hash TEXT",
            "CREATE INDEX IF NOT EXISTS questions_pattern_hash_idx ON questions(pattern_id, question_hash)",
            """
            CREATE TABLE IF NOT EXISTS mistake_book (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id),
                pattern_id INT REFERENCES patterns(id),
                question_text TEXT NOT NULL,
                question_hash TEXT NOT NULL,
                options JSONB NOT NULL,
                correct_option_index INT NOT NULL,
                selected_option_index INT,
                explanation TEXT,
                difficulty INT DEFAULT 3,
                status TEXT DEFAULT 'open',
                missed_count INT DEFAULT 1,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                last_missed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                last_reviewed_at TIMESTAMP WITH TIME ZONE,
                UNIQUE(user_id, question_hash)
            )
            """,
            "CREATE INDEX IF NOT EXISTS mistake_book_user_status_idx ON mistake_book(user_id, status, last_missed_at DESC)",
            """
            CREATE TABLE IF NOT EXISTS user_reminder_settings (
                user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
                enabled BOOLEAN DEFAULT FALSE,
                reminder_time TEXT DEFAULT '20:00',
                timezone TEXT DEFAULT 'Asia/Kolkata',
                last_reminded_at TIMESTAMP WITH TIME ZONE,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
            """,
        ]
        for statement in statements:
            self.execute_query(statement)

    @staticmethod
    def question_hash(question_text):
        normalized = " ".join(str(question_text or "").lower().split())
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get_user(self, user_id):
        return self.execute_query("SELECT * FROM users WHERE user_id = %s", (user_id,))

    def register_user(self, user_id, username, first_name, last_name):
        query = """
        INSERT INTO users (user_id, username, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            username = COALESCE(EXCLUDED.username, users.username),
            first_name = COALESCE(EXCLUDED.first_name, users.first_name),
            last_name = COALESCE(EXCLUDED.last_name, users.last_name)
        """
        return self.execute_query(query, (user_id, username, first_name, last_name)) is not None

    def get_categories(self):
        return self.execute_query("SELECT * FROM categories")

    def get_topics(self, category_id):
        query = """
        SELECT DISTINCT t.*
        FROM topics t
        JOIN patterns p ON p.topic_id = t.id
        WHERE t.category_id = %s AND p.is_unlocked = TRUE
        ORDER BY t.id
        """
        return self.execute_query(query, (category_id,))

    def get_patterns(self, topic_id):
        return self.execute_query("SELECT * FROM patterns WHERE topic_id = %s AND is_unlocked = TRUE ORDER BY id", (topic_id,))
        
    def get_all_pattern_ids_for_topic(self, topic_id):
        res = self.execute_query("SELECT id FROM patterns WHERE topic_id = %s AND is_unlocked = TRUE ORDER BY id", (topic_id,))
        return [row['id'] for row in res] if res else []

    def get_all_pattern_ids_for_category(self, category_id):
        query = """
        SELECT p.id 
        FROM patterns p
        JOIN topics t ON p.topic_id = t.id
        WHERE t.category_id = %s AND p.is_unlocked = TRUE
        ORDER BY p.id
        """
        res = self.execute_query(query, (category_id,))
        return [row['id'] for row in res] if res else []

    def unlock_pattern(self, pattern_id):
        self.execute_query("UPDATE patterns SET is_unlocked = %s WHERE id = %s", (True, pattern_id))

    def save_question(self, pattern_id, question_text, options, correct_index, explanation, difficulty):
        query = """
        INSERT INTO questions (pattern_id, question_text, question_hash, options, correct_option_index, explanation, difficulty)
        SELECT %s, %s, %s, %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM questions
            WHERE pattern_id = %s AND question_hash = %s
        )
        """
        # Explicit serialization because psycopg2 might default a Python list to text[] instead of jsonb
        options_json = json.dumps(options)
        q_hash = self.question_hash(question_text)
        self.execute_query(
            query,
            (pattern_id, question_text, q_hash, options_json, correct_index, explanation, difficulty, pattern_id, q_hash),
        )

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

    def record_question_attempt(self, user_id, pattern_id, is_correct, time_taken_seconds):
        query = """
        INSERT INTO question_attempts (user_id, pattern_id, is_correct, time_taken_seconds)
        VALUES (%s, %s, %s, %s)
        """
        self.execute_query(query, (user_id, pattern_id, is_correct, time_taken_seconds))

    def record_mistake(self, user_id, pattern_id, question_text, options, correct_index, selected_index, explanation, difficulty=3):
        query = """
        INSERT INTO mistake_book (
            user_id, pattern_id, question_text, question_hash, options, correct_option_index,
            selected_option_index, explanation, difficulty
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_id, question_hash) DO UPDATE SET
            pattern_id = EXCLUDED.pattern_id,
            options = EXCLUDED.options,
            correct_option_index = EXCLUDED.correct_option_index,
            selected_option_index = EXCLUDED.selected_option_index,
            explanation = EXCLUDED.explanation,
            difficulty = EXCLUDED.difficulty,
            status = 'open',
            missed_count = mistake_book.missed_count + 1,
            last_missed_at = CURRENT_TIMESTAMP
        """
        self.execute_query(
            query,
            (
                user_id,
                pattern_id,
                question_text,
                self.question_hash(question_text),
                json.dumps(options),
                correct_index,
                selected_index,
                explanation,
                difficulty,
            ),
        )

    def mark_mistake_reviewed(self, user_id, mistake_id):
        query = """
        UPDATE mistake_book
        SET status = 'reviewed', last_reviewed_at = CURRENT_TIMESTAMP
        WHERE user_id = %s AND id = %s
        """
        return self.execute_query(query, (user_id, mistake_id))

    def get_mistake_book(self, user_id, limit=20):
        query = """
        SELECT
            mb.id,
            mb.pattern_id,
            mb.question_text,
            mb.options,
            mb.correct_option_index,
            mb.selected_option_index,
            mb.explanation,
            mb.difficulty,
            mb.status,
            mb.missed_count,
            mb.last_missed_at,
            p.name as pattern_name,
            t.name as topic_name
        FROM mistake_book mb
        LEFT JOIN patterns p ON p.id = mb.pattern_id
        LEFT JOIN topics t ON t.id = p.topic_id
        WHERE mb.user_id = %s AND mb.status = 'open'
        ORDER BY mb.last_missed_at DESC
        LIMIT %s
        """
        return self.execute_query(query, (user_id, limit)) or []

    def get_mistake_pattern_ids(self, user_id, limit=10):
        query = """
        SELECT pattern_id, COUNT(*) as wrong_count
        FROM mistake_book
        WHERE user_id = %s AND status = 'open' AND pattern_id IS NOT NULL
        GROUP BY pattern_id
        ORDER BY wrong_count DESC, MAX(last_missed_at) DESC
        LIMIT %s
        """
        rows = self.execute_query(query, (user_id, limit)) or []
        return [row["pattern_id"] for row in rows]
        
    def get_today_solved_count(self, user_id):
        query = """
        SELECT COUNT(*) as count 
        FROM question_attempts 
        WHERE user_id = %s AND created_at >= CURRENT_DATE
        """
        res = self.execute_query(query, (user_id,))
        return res[0]['count'] if res else 0

    def get_unlock_progress(self, user_id):
        topic_query = """
        SELECT
            t.id as topic_id,
            t.name as topic_name,
            c.name as category_name,
            COUNT(p.id) as total_patterns,
            COUNT(up.pattern_id) as practiced_patterns,
            COUNT(CASE WHEN up.mastery_score >= 0.8 THEN 1 END) as mastered_patterns,
            COALESCE(AVG(up.mastery_score), 0) as avg_mastery
        FROM topics t
        JOIN categories c ON c.id = t.category_id
        JOIN patterns p ON p.topic_id = t.id AND p.is_unlocked = TRUE
        LEFT JOIN user_progress up ON up.pattern_id = p.id AND up.user_id = %s
        GROUP BY t.id, t.name, c.name
        ORDER BY c.name, t.name
        """
        pattern_query = """
        SELECT
            p.id,
            p.name,
            t.name as topic_name,
            COALESCE(up.mastery_score, 0) as mastery_score,
            COALESCE(up.total_attempts, 0) as total_attempts,
            COALESCE(up.correct_attempts, 0) as correct_attempts
        FROM patterns p
        JOIN topics t ON t.id = p.topic_id
        LEFT JOIN user_progress up ON up.pattern_id = p.id AND up.user_id = %s
        WHERE p.is_unlocked = TRUE
        ORDER BY p.id
        """
        return {
            "topics": self.execute_query(topic_query, (user_id,)) or [],
            "patterns": self.execute_query(pattern_query, (user_id,)) or [],
        }

    def get_reminder_settings(self, user_id):
        query = """
        INSERT INTO user_reminder_settings (user_id)
        VALUES (%s)
        ON CONFLICT (user_id) DO NOTHING
        """
        self.execute_query(query, (user_id,))
        rows = self.execute_query(
            "SELECT user_id, enabled, reminder_time, timezone, last_reminded_at FROM user_reminder_settings WHERE user_id = %s",
            (user_id,),
        )
        return rows[0] if rows else None

    def upsert_reminder_settings(self, user_id, enabled, reminder_time, timezone="Asia/Kolkata"):
        query = """
        INSERT INTO user_reminder_settings (user_id, enabled, reminder_time, timezone, updated_at)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id) DO UPDATE SET
            enabled = EXCLUDED.enabled,
            reminder_time = EXCLUDED.reminder_time,
            timezone = EXCLUDED.timezone,
            updated_at = CURRENT_TIMESTAMP
        RETURNING user_id, enabled, reminder_time, timezone, last_reminded_at
        """
        rows = self.execute_query(query, (user_id, enabled, reminder_time, timezone))
        return rows[0] if rows else None

    def get_enabled_reminder_settings(self):
        return self.execute_query(
            """
            SELECT rs.user_id, rs.reminder_time, rs.timezone, rs.last_reminded_at, u.first_name
            FROM user_reminder_settings rs
            JOIN users u ON u.user_id = rs.user_id
            WHERE rs.enabled = TRUE
            """
        ) or []

    def mark_reminder_sent(self, user_id):
        return self.execute_query(
            "UPDATE user_reminder_settings SET last_reminded_at = CURRENT_TIMESTAMP WHERE user_id = %s",
            (user_id,),
        )

    def get_current_difficulty(self, user_id, pattern_id):
        res = self.execute_query(
            """
            SELECT
                p.difficulty_level,
                t.name as topic_name,
                up.last_difficulty_level,
                up.total_attempts,
                up.correct_attempts
            FROM patterns p
            JOIN topics t ON p.topic_id = t.id
            LEFT JOIN user_progress up ON up.pattern_id = p.id AND up.user_id = %s
            WHERE p.id = %s
            """,
            (user_id, pattern_id),
        )
        if not res:
            return 2

        row = res[0]
        base_difficulty = row.get('difficulty_level') or 2
        current_difficulty = row.get('last_difficulty_level') or base_difficulty

        if (row.get('topic_name') or '').strip().lower() == 'vedic math':
            attempts = row.get('total_attempts') or 0
            correct = row.get('correct_attempts') or 0
            accuracy = (correct / attempts) if attempts else 0
            if attempts < 3:
                return 1
            if attempts < 7:
                return min(2, current_difficulty)
            if attempts < 12 or accuracy < 0.7:
                return min(3, current_difficulty)

        return current_difficulty

    def add_pattern(self, topic_id, name, description, difficulty, user_id=None):
        query = """
        INSERT INTO patterns (topic_id, name, description, difficulty_level, is_unlocked)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (topic_id, name) DO UPDATE SET
            description = EXCLUDED.description,
            difficulty_level = EXCLUDED.difficulty_level,
            is_unlocked = EXCLUDED.is_unlocked
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

    def sync_9_day_cycle(self, user_id):
        """Ensure all unlocked patterns are tracked in user_added_patterns for the 9-day rule."""
        query = """
        INSERT INTO user_added_patterns (user_id, pattern_id)
        SELECT %s, id FROM patterns 
        WHERE is_unlocked = TRUE
        ON CONFLICT (user_id, pattern_id) DO NOTHING
        """
        self.execute_query(query, (user_id,))

    def get_new_patterns_in_cycle(self, user_id):
        """Patterns added in the last 9 days."""
        query = """
        SELECT p.*, t.name as topic_name, uap.added_at
        FROM user_added_patterns uap
        JOIN patterns p ON uap.pattern_id = p.id
        JOIN topics t ON p.topic_id = t.id
        WHERE uap.user_id = %s 
        AND p.is_unlocked = TRUE
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
        AND p.is_unlocked = TRUE
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
