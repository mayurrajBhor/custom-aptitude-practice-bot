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
    options JSONB NOT NULL,
    correct_option_index INT NOT NULL,
    explanation TEXT,
    difficulty INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User Progress and SRS
CREATE TABLE IF NOT EXISTS user_progress (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    pattern_id INT REFERENCES patterns(id),
    mastery_score FLOAT DEFAULT 0.0,
    total_attempts INT DEFAULT 0,
    correct_attempts INT DEFAULT 0,
    last_practiced_at TIMESTAMP WITH TIME ZONE,
    next_review_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    srs_interval INT DEFAULT 1,
    easiness_factor FLOAT DEFAULT 2.5,
    avg_time_seconds FLOAT DEFAULT 0.0,
    last_difficulty_level INT DEFAULT 1
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
    session_type TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    score INT,
    total_questions INT
);

-- Insert Initial Categories
INSERT INTO categories (name) VALUES ('Quant'), ('Reasoning'), ('Data Insights') ON CONFLICT (name) DO NOTHING;
