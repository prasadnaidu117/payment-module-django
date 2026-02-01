-- schema.sql (PostgreSQL compatible)
 
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'pending', 'success', 'failed', 'refunded'
    transaction_id VARCHAR(255) UNIQUE, -- From external gateway stub
    idempotency_key VARCHAR(255) UNIQUE, -- For handling duplicate requests
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
 
CREATE INDEX IF NOT EXISTS idx_payments_order_id
ON payments(order_id);