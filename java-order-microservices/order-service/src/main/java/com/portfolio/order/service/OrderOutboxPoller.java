package com.portfolio.order.service;

import java.util.concurrent.atomic.AtomicInteger;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.portfolio.order.messaging.SqsEventPublisher;
import com.portfolio.order.persistence.OrderOutboxRepository;

/**
 * Polls the order_outbox table for unsent events and publishes them to SQS.
 * Runs every 5 seconds to drain the outbox with low latency.
 *
 * This ensures that the database and SQS event stream stay in sync:
 * - If DB commit succeeds but SQS publish fails, the event stays in the outbox.
 * - The next poll will retry publishing.
 * - Only after successful SQS publish is the event marked as sent.
 */
@Service
@EnableScheduling
public class OrderOutboxPoller {
	private static final Logger log = LoggerFactory.getLogger(OrderOutboxPoller.class);

	private final OrderOutboxRepository outboxRepository;
	private final SqsEventPublisher sqsEventPublisher;
	private final ObjectMapper objectMapper;
	private final String ordersQueueUrl;

	public OrderOutboxPoller(
			OrderOutboxRepository outboxRepository,
			SqsEventPublisher sqsEventPublisher,
			ObjectMapper objectMapper,
			@Value("${app.sqs.queue.orders.url:}") String ordersQueueUrl
	) {
		this.outboxRepository = outboxRepository;
		this.sqsEventPublisher = sqsEventPublisher;
		this.objectMapper = objectMapper;
		this.ordersQueueUrl = ordersQueueUrl;
	}

	/**
	 * Poll outbox table every 5 seconds and publish unsent events.
	 */
	@Scheduled(fixedDelay = 5000, initialDelay = 5000)
	@Transactional
	public void pollAndPublish() {
		var unsent = outboxRepository.findUnsentEvents();
		if (unsent.isEmpty()) {
			return; // Nothing to do
		}

		log.debug("Found {} unsent outbox events", unsent.size());
		AtomicInteger published = new AtomicInteger(0);

		unsent.forEach(event -> {
			try {
				// Parse the payload back to an object
				var eventPayload = objectMapper.readValue(event.getPayload(), Object.class);

				// Publish to SQS
				sqsEventPublisher.publish(ordersQueueUrl, eventPayload);

				// Mark as sent
				event.markAsSent();
				outboxRepository.save(event);
				published.incrementAndGet();

				log.debug("Published outbox event: id={}, type={}, aggregateId={}",
						event.getId(), event.getEventType(), event.getAggregateId());
			} catch (Exception ex) {
				log.warn("Failed to publish outbox event: id={}, type={}, aggregateId={}, error={}",
						event.getId(), event.getEventType(), event.getAggregateId(), ex.getMessage());
				// Don't mark as sent so it will be retried on the next poll
			}
		});

		if (published.get() > 0) {
			log.info("Published {} outbox events to SQS", published.get());
		}
	}
}
