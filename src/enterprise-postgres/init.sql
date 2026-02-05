-- Example initialization script for enterprise PostgreSQL
-- This script creates a sample table and inserts some data

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email) VALUES 
    ('admin_user', 'admin@example.com'),
    ('demo_user', 'demo@example.com')
ON CONFLICT (username) DO NOTHING;

-- Create a sample configuration table
CREATE TABLE IF NOT EXISTS app_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);