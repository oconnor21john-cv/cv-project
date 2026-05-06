package com.portfolio.order.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.Map;
import java.util.UUID;

import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.portfolio.order.api.CreateOrderRequest;
import com.portfolio.order.domain.OrderStatus;
import com.portfolio.order.events.OrderCancelledEvent;
import com.portfolio.order.events.OrderConfirmedEvent;
import com.portfolio.order.events.OrderPlacedEvent;
import com.portfolio.order.messaging.OrderOutboxPublisher;
import com.portfolio.order.persistence.OrderEntity;
import com.portfolio.order.persistence.OrderRepository;

/**
 * Handles all transactional write operations for orders.
 * Separated from OrderService to ensure AOP proxy is correctly applied
 * when calling @Transactional methods from non-transactional callers.
 *
 * Uses the outbox pattern for event publishing: events are written to the
 * order_outbox table within the same transaction as the main data.
 * A scheduled OrderOutboxPoller then reads and publishes them to SQS.
 * This ensures transactional consistency between the database and event stream.
 */
@Component
public class OrderTransactionalWriter {
	private static final Logger log = LoggerFactory.getLogger(OrderTransactionalWriter.class);

	private final OrderRepository orderRepository;
	private final OrderOutboxPublisher outboxPublisher;

	public OrderTransactionalWriter(
			OrderRepository orderRepository,
			OrderOutboxPublisher outboxPublisher
	) {
		this.orderRepository = orderRepository;
		this.outboxPublisher = outboxPublisher;
	}

	/**
	 * Creates a new order within a transaction.
	 * Called after price lookup to keep HTTP calls outside the transaction.
	 */
	@Transactional
	public OrderEntity createTransactional(CreateOrderRequest request, String username,
			Map<String, BigDecimal> prices) {
		var orderId = UUID.randomUUID();

		var total = request.items().stream()
				.map(i -> prices.get(i.sku()).multiply(BigDecimal.valueOf(i.quantity())))
				.reduce(BigDecimal.ZERO, BigDecimal::add);

		var order = new OrderEntity(orderId, total, username);
		request.items().forEach(i -> order.addItem(i.sku(), i.quantity(), prices.get(i.sku())));
		orderRepository.save(order);

		var event = new OrderPlacedEvent(
				UUID.randomUUID(),
				Instant.now(),
				order.getId(),
				order.getTotalAmount(),
				order.getItems().stream()
						.map(i -> new OrderPlacedEvent.Item(i.getSku(), i.getQuantity(), i.getUnitPrice()))
						.toList()
		);
		outboxPublisher.publishEvent(event, "OrderPlacedEvent");

		log.info("Order created: orderId={}, total={}, user={}", orderId, total, username);
		return order;
	}

	/**
	 * Updates order status to CONFIRMED and publishes confirmation event.
	 * Called after successful inventory reservation and payment.
	 */
	@Transactional
	public void confirmOrder(OrderEntity order) {
		order.setStatus(OrderStatus.CONFIRMED);
		log.info("Order confirmed: orderId={}, total={}", order.getId(), order.getTotalAmount());
		var event = new OrderConfirmedEvent(UUID.randomUUID(), Instant.now(), order.getId(), order.getTotalAmount());
		outboxPublisher.publishEvent(event, "OrderConfirmedEvent");
	}

	/**
	 * Updates order status to STOCK_FAILED and publishes cancellation event.
	 */
	@Transactional
	public void failStock(OrderEntity order, String reason) {
		order.setStatus(OrderStatus.STOCK_FAILED);
		var event = new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), order.getId(), reason);
		outboxPublisher.publishEvent(event, "OrderCancelledEvent");
	}

	/**
	 * Updates order status to PAYMENT_FAILED and publishes cancellation event.
	 */
	@Transactional
	public void failPayment(OrderEntity order, String reason) {
		order.setStatus(OrderStatus.PAYMENT_FAILED);
		var event = new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), order.getId(), reason);
		outboxPublisher.publishEvent(event, "OrderCancelledEvent");
	}

	/**
	 * Cancels a PLACED order.
	 */
	@Transactional
	public void cancelPlaced(OrderEntity order) {
		order.setStatus(OrderStatus.CANCELLED);
		publishCancelled(order.getId(), "Cancelled by user");
		log.info("Order cancelled (was PLACED): orderId={}", order.getId());
	}

	/**
	 * Cancels a CONFIRMED order.
	 */
	@Transactional
	public void cancelConfirmed(OrderEntity order) {
		order.setStatus(OrderStatus.CANCELLED);
		publishCancelled(order.getId(), "Cancelled by user (stock released)");
		log.info("Order cancelled (was CONFIRMED): orderId={}", order.getId());
	}

	/**
	 * Deletes all orders for a given user.
	 */
	@Transactional
	public void deleteAllByUser(String username) {
		orderRepository.deleteByCreatedBy(username);
	}

	private void publishCancelled(UUID orderId, String reason) {
		var event = new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), orderId, reason);
		outboxPublisher.publishEvent(event, "OrderCancelledEvent");
	}
}
