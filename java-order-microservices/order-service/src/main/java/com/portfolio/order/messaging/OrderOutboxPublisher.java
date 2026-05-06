package com.portfolio.order.messaging;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.portfolio.order.persistence.OrderOutboxEntity;
import com.portfolio.order.persistence.OrderOutboxRepository;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/**
 * Publishes events to the outbox table instead of directly to SQS.
 * This enables the outbox pattern for transactional event publishing.
 */
@Component
public class OrderOutboxPublisher {
	private static final Logger log = LoggerFactory.getLogger(OrderOutboxPublisher.class);

	private final OrderOutboxRepository outboxRepository;
	private final ObjectMapper objectMapper;

	public OrderOutboxPublisher(
			OrderOutboxRepository outboxRepository,
			ObjectMapper objectMapper
	) {
		this.outboxRepository = outboxRepository;
		this.objectMapper = objectMapper;
	}

	/**
	 * Write an event to the outbox table.
	 * The event will be published to SQS by the OrderOutboxPoller.
	 */
	public void publishEvent(Object event, String eventType) {
		try {
			var payload = objectMapper.writeValueAsString(event);

			// Determine the aggregate ID (order ID) from the event
			var aggregateId = extractAggregateId(event);

			var outboxEvent = new OrderOutboxEntity(aggregateId, eventType, payload);
			outboxRepository.save(outboxEvent);

			log.debug("Event written to outbox: type={}, aggregateId={}", eventType, aggregateId);
		} catch (Exception ex) {
			log.error("Failed to write event to outbox: type={}, error={}", eventType, ex.getMessage(), ex);
			throw new RuntimeException("Failed to publish event to outbox", ex);
		}
	}

	/**
	 * Extract the aggregate ID (order ID) from the event.
	 * Handles the known event types that have an orderId or id field.
	 */
	private java.util.UUID extractAggregateId(Object event) throws Exception {
		// Try to get the orderId field first (most events have this)
		try {
			var field = event.getClass().getDeclaredField("orderId");
			field.setAccessible(true);
			var id = field.get(event);
			if (id instanceof java.util.UUID) {
				return (java.util.UUID) id;
			}
		} catch (NoSuchFieldException ex) {
			// Field doesn't exist, try next approach
		}

		// For PaymentSucceededEvent, PaymentFailedEvent, try orderId
		try {
			var method = event.getClass().getMethod("orderId");
			var id = method.invoke(event);
			if (id instanceof java.util.UUID) {
				return (java.util.UUID) id;
			}
		} catch (Exception ex) {
			// Method doesn't exist
		}

		// Fallback: use a generated UUID if we can't extract the aggregate ID
		log.warn("Could not extract aggregateId from event of type {}, using random UUID",
				event.getClass().getSimpleName());
		return java.util.UUID.randomUUID();
	}
}
