package com.portfolio.order.persistence;

import java.time.Instant;
import java.util.UUID;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * Outbox pattern: write events to the database in the same transaction as the main data.
 * A scheduled poller reads unsent events and publishes them to SQS, then marks them as sent.
 * This ensures transactional consistency between the database and the event stream.
 */
@Entity
@Table(name = "order_outbox")
public class OrderOutboxEntity {
	@Id
	private UUID id;

	@Column(nullable = false, name = "aggregate_id")
	private UUID aggregateId;

	@Column(nullable = false, name = "event_type", length = 255)
	private String eventType;

	@Column(nullable = false)
	private String payload;

	@Column(nullable = false)
	private boolean sent;

	@Column(nullable = false, name = "created_at")
	private Instant createdAt;

	@Column(name = "sent_at")
	private Instant sentAt;

	protected OrderOutboxEntity() {
	}

	public OrderOutboxEntity(UUID aggregateId, String eventType, String payload) {
		this.id = UUID.randomUUID();
		this.aggregateId = aggregateId;
		this.eventType = eventType;
		this.payload = payload;
		this.sent = false;
		this.createdAt = Instant.now();
	}

	// Getters
	public UUID getId() {
		return id;
	}

	public UUID getAggregateId() {
		return aggregateId;
	}

	public String getEventType() {
		return eventType;
	}

	public String getPayload() {
		return payload;
	}

	public boolean isSent() {
		return sent;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}

	public Instant getSentAt() {
		return sentAt;
	}

	// Setters
	public void markAsSent() {
		this.sent = true;
		this.sentAt = Instant.now();
	}
}
