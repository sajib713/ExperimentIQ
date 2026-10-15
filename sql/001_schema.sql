-- Generated technical key = 1-based CSV line position, NOT provided customer ID.
-- Run via: psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f sql/001_schema.sql
BEGIN;
CREATE TABLE IF NOT EXISTS experiment_customers (
    source_row_number BIGINT PRIMARY KEY CHECK(source_row_number>0),
    recency SMALLINT NOT NULL CHECK (recency BETWEEN 1 AND 12),
    history_segment TEXT NOT NULL,
    history NUMERIC(15,2) NOT NULL CHECK (history>=0),
    mens SMALLINT NOT NULL CHECK(mens IN (0,1)),
    womens SMALLINT NOT NULL CHECK(womens IN (0,1)),
    zip_code TEXT NOT NULL CHECK(zip_code IN ('Urban','Suburban','Rural')),
    newbie SMALLINT NOT NULL CHECK(newbie IN(0,1)),
    channel TEXT NOT NULL CHECK(channel IN ('Web','Phone','Multichannel')),
    segment TEXT NOT NULL CHECK(segment IN ('No E-Mail','Mens E-Mail','Womens E-Mail')),
    visit SMALLINT NOT NULL CHECK(visit IN(0,1)),
    conversion SMALLINT NOT NULL CHECK(conversion IN(0,1)),
    spend NUMERIC(15,2) NOT NULL CHECK(spend>=0)
);
CREATE INDEX IF NOT EXISTS idx_experiment_customers_segment ON experiment_customers(segment);
CREATE INDEX IF NOT EXISTS idx_experiment_customers_channel ON experiment_customers(channel);
CREATE INDEX IF NOT EXISTS idx_experiment_customers_zip ON experiment_customers(zip_code);
COMMIT;
