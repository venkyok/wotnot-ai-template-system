-- Database initialization script for Wotnot
-- This script sets up the initial database structure

-- Create the main database (if not exists)
CREATE DATABASE IF NOT EXISTS wotnot;

-- Switch to the wotnot database
\c wotnot;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create basic schema (tables will be created by SQLAlchemy)
-- This is just for initial setup

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE wotnot TO postgres;