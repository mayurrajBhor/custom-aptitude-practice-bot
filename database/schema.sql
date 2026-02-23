-- GMAT Practice Bot Schema

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
    name TEXT UNIQUE NOT NULL -- 'Quant', 'Reasoning', 'Data Insights'
);

-- Topics (linked to categories)
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id),
    name TEXT NOT NULL,
    description TEXT,
    UNIQUE(category_id, name)
);

-- Patterns (Specific question types within topics)
CREATE TABLE IF NOT EXISTS patterns (
    id SERIAL PRIMARY KEY,
    topic_id INT REFERENCES topics(id),
    name TEXT NOT NULL,
    description TEXT,
    difficulty_level INT DEFAULT 1, -- 1 to 5
    is_unlocked BOOLEAN DEFAULT FALSE, -- Some might be locked by default
    prompt_guideline TEXT, -- Specific instructions for LLM to generate this pattern
    UNIQUE(topic_id, name)
);

-- Generated Questions
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    pattern_id INT REFERENCES patterns(id),
    question_text TEXT NOT NULL,
    options JSONB NOT NULL, -- list of strings
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
    mastery_score FLOAT DEFAULT 0.0, -- 0 to 1
    total_attempts INT DEFAULT 0,
    correct_attempts INT DEFAULT 0,
    last_practiced_at TIMESTAMP WITH TIME ZONE,
    next_review_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    srs_interval INT DEFAULT 1, -- Days
    easiness_factor FLOAT DEFAULT 2.5
);

-- Practice Sessions
CREATE TABLE IF NOT EXISTS practice_sessions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id),
    session_type TEXT, -- 'daily', 'custom'
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    score INT,
    total_questions INT
);

-- Insert Initial Categories
INSERT INTO categories (name) VALUES ('Quant'), ('Reasoning'), ('Data Insights') ON CONFLICT DO NOTHING;
