-- GMAT Practice Bot Schema for SQLite

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    daily_goal INTEGER DEFAULT 10,
    is_premium BOOLEAN DEFAULT 0
);

-- Categories (Quant, Reasoning, Data Insights)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Topics
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER REFERENCES categories(id),
    name TEXT NOT NULL,
    description TEXT,
    UNIQUE(category_id, name)
);

-- Patterns
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER REFERENCES topics(id),
    name TEXT NOT NULL,
    description TEXT,
    difficulty_level INTEGER DEFAULT 1,
    is_unlocked BOOLEAN DEFAULT 0,
    prompt_guideline TEXT,
    UNIQUE(topic_id, name)
);

-- Questions
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_id INTEGER REFERENCES patterns(id),
    question_text TEXT NOT NULL,
    options TEXT NOT NULL, -- JSON string
    correct_option_index INTEGER NOT NULL,
    explanation TEXT,
    difficulty INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User Progress and SRS
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    pattern_id INTEGER REFERENCES patterns(id),
    mastery_score REAL DEFAULT 0.0,
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    last_practiced_at DATETIME,
    next_review_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    srs_interval INTEGER DEFAULT 1,
    easiness_factor REAL DEFAULT 2.5,
    avg_time_seconds REAL DEFAULT 0.0,
    last_difficulty_level INTEGER DEFAULT 1
);

-- Tracking when a user adds a pattern for the 9-day rule
CREATE TABLE IF NOT EXISTS user_added_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    pattern_id INTEGER REFERENCES patterns(id),
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, pattern_id)
);

-- Practice Sessions
CREATE TABLE IF NOT EXISTS practice_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users(user_id),
    session_type TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    score INTEGER,
    total_questions INTEGER
);

-- Insert Initial Categories
INSERT OR IGNORE INTO categories (name) VALUES ('Quant'), ('Reasoning'), ('Data Insights');
