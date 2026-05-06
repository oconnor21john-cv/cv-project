-- Outbox table for transactional event publishing
-- Events are written to this table within the same DB transaction as the main business data.
-- A scheduled job then reads unsent events and publishes them to SQS.
CREATE TABLE order_outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload TEXT NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP
);

-- Index for finding unsent events (used by the scheduled job)
CREATE INDEX idx_order_outbox_sent_created ON order_outbox(sent, created_at);

-- Index for finding events by aggregate ID (for debugging/auditing)
CREATE INDEX idx_order_outbox_aggregate_id ON order_outbox(aggregate_id);
