-- Enable required extensions for TimescaleDB and pgvector in PostgreSQL 16
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'NEPSE Cognitive Triad extensions initialized: timescaledb, vector, uuid-ossp';
END $$;
