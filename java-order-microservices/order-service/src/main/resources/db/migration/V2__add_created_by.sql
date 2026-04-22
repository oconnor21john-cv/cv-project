ALTER TABLE orders ADD COLUMN created_by TEXT NOT NULL DEFAULT 'unknown';
CREATE INDEX idx_orders_created_by ON orders(created_by);
