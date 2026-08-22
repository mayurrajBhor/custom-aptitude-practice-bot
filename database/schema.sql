-- GMAT Practice Bot Schema (PostgreSQL)

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    daily_goal INT DEFAULT 10,
    is_premium BOOLEAN DEFAULT FALSE
);

-- Categories (Quant, Reasoning, Data Insights)
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Topics
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    name TEXT NOT NULL,
    description TEXT,
    UNIQUE(category_id, name)
);

-- Patterns
CREATE TABLE IF NOT EXISTS patterns (
    id SERIAL PRIMARY KEY,
    topic_id INT REFERENCES topics(id),
    name TEXT NOT NULL,
    description TEXT,
    difficulty_level INT DEFAULT 1,
    is_unlocked BOOLEAN DEFAULT FALSE,
    prompt_guideline TEXT,
    UNIQUE(topic_id, name)
);

-- Questions
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    pattern_id INT REFERENCES patterns(id),
    question_text TEXT NOT NULL,
    question_hash TEXT,
    options JSONB NOT NULL,
    correct_option_index INT NOT NULL,
    explanation TEXT,
    difficulty INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS questions_pattern_hash_idx ON questions(pattern_id, question_hash);

-- User Progress and SRS
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    pattern_id INT REFERENCES patterns(id),
    mastery_score FLOAT DEFAULT 0.0,
    total_attempts INT DEFAULT 0,
    correct_attempts INT DEFAULT 0,
    wrong_attempts INT DEFAULT 0,
    last_practiced_at TIMESTAMP WITH TIME ZONE,
    next_review_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    srs_interval INT DEFAULT 1,
    easiness_factor FLOAT DEFAULT 2.5,
    avg_time_seconds FLOAT DEFAULT 0.0,
    last_difficulty_level INT DEFAULT 1,
    UNIQUE(user_id, pattern_id)
);

-- Tracking when a user adds a pattern for the 9-day rule
CREATE TABLE IF NOT EXISTS user_added_patterns (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    pattern_id INT REFERENCES patterns(id),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, pattern_id)
);

-- Practice Sessions
CREATE TABLE IF NOT EXISTS practice_sessions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    session_uuid TEXT UNIQUE,
    session_type TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    stopped_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'active',
    score INT,
    total_questions INT,
    planned_total_questions INT,
    pattern_ids JSONB,
    pattern_names JSONB
);

-- Question Attempts (Timing and specific history)
CREATE TABLE IF NOT EXISTS question_attempts (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    pattern_id INT REFERENCES patterns(id),
    session_uuid TEXT,
    question_number INT,
    question_text TEXT,
    question_hash TEXT,
    options JSONB,
    correct_option_index INT,
    selected_option_index INT,
    explanation TEXT,
    difficulty INT,
    is_correct BOOLEAN NOT NULL,
    is_skipped BOOLEAN DEFAULT FALSE,
    time_taken_seconds FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS question_attempts_user_created_idx ON question_attempts(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS question_attempts_session_idx ON question_attempts(session_uuid, question_number);

-- Mistake book keeps concrete wrong questions for later review/practice.
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
);

CREATE INDEX IF NOT EXISTS mistake_book_user_status_idx ON mistake_book(user_id, status, last_missed_at DESC);

-- Smart reminder preferences used by the Telegram bot reminder job.
CREATE TABLE IF NOT EXISTS user_reminder_settings (
    user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
    enabled BOOLEAN DEFAULT FALSE,
    reminder_time TEXT DEFAULT '20:00',
    timezone TEXT DEFAULT 'Asia/Kolkata',
    last_reminded_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert Initial Categories
INSERT INTO categories (name) VALUES ('Quant'), ('Reasoning'), ('Data Insights') ON CONFLICT (name) DO NOTHING;
