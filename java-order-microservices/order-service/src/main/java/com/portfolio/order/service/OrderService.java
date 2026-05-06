package com.portfolio.order.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClientResponseException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.portfolio.order.api.CreateOrderRequest;
import com.portfolio.order.api.OrderAccessDeniedException;
import com.portfolio.order.api.OrderNotFoundException;
import com.portfolio.order.clients.InventoryClient;
import com.portfolio.order.clients.InventoryReserveRequest;
import com.portfolio.order.clients.InventoryReserveRequestItem;
import com.portfolio.order.clients.PaymentClient;
import com.portfolio.order.clients.PaymentCreateRequest;
import com.portfolio.order.domain.OrderStatus;
import com.portfolio.order.events.OrderCancelledEvent;
import com.portfolio.order.events.OrderConfirmedEvent;
import com.portfolio.order.events.OrderPlacedEvent;
import com.portfolio.order.messaging.SqsEventPublisher;
import com.portfolio.order.persistence.OrderEntity;
import com.portfolio.order.persistence.OrderRepository;

@Service
public class OrderService {
	private static final Logger log = LoggerFactory.getLogger(OrderService.class);

	private final OrderRepository orderRepository;
	private final InventoryClient inventoryClient;
	private final PaymentClient paymentClient;
	private final SqsEventPublisher sqsEventPublisher;
	private final String ordersQueueUrl;

	public OrderService(
			OrderRepository orderRepository,
			InventoryClient inventoryClient,
			PaymentClient paymentClient,
			SqsEventPublisher sqsEventPublisher,
			@Value("${app.sqs.queue.orders.url:}") String ordersQueueUrl
	) {
		this.orderRepository = orderRepository;
		this.inventoryClient = inventoryClient;
		this.paymentClient = paymentClient;
		this.sqsEventPublisher = sqsEventPublisher;
		this.ordersQueueUrl = ordersQueueUrl;
	}

	/**
	 * Creates a new order. Price lookup happens before the transaction opens
	 * so that the HTTP call to inventory-service does not hold a DB connection.
	 */
	public OrderEntity create(CreateOrderRequest request, String username) {
		var skus = request.items().stream().map(i -> i.sku()).toList();
		var prices = inventoryClient.fetchPrices(skus);

		log.info("Creating order for user={} with {} item(s)", username, request.items().size());
		return createTransactional(request, username, prices);
	}

	@Transactional
	protected OrderEntity createTransactional(CreateOrderRequest request, String username,
			java.util.Map<String, BigDecimal> prices) {
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
		sqsEventPublisher.publish(ordersQueueUrl, event);

		log.info("Order created: orderId={}, total={}, user={}", orderId, total, username);
		return order;
	}

	@Transactional
	public OrderEntity confirm(UUID orderId, String username) {
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new OrderNotFoundException(orderId));
		verifyOwnership(order, username);

		if (order.getStatus() != OrderStatus.PLACED) {
			log.debug("Confirm ignored: orderId={} already in status {}", orderId, order.getStatus());
			return order;
		}

		log.info("Confirming order: orderId={}, user={}", orderId, username);

		var reserveReq = new InventoryReserveRequest(
				orderId,
				order.getItems().stream()
						.map(i -> new InventoryReserveRequestItem(i.getSku(), i.getQuantity()))
						.toList()
		);

		try {
			var reserveResp = inventoryClient.reserve(reserveReq);
			if (reserveResp == null || !"RESERVED".equalsIgnoreCase(reserveResp.status())) {
				log.warn("Stock reservation failed: orderId={}, reason={}", orderId,
						reserveResp == null ? "Inventory error" : reserveResp.message());
				return failStock(order, reserveResp == null ? "Inventory error" : reserveResp.message());
			}
		} catch (RestClientResponseException ex) {
			log.warn("Inventory call failed: orderId={}, status={}", orderId, ex.getStatusCode());
			return failStock(order, "Inventory call failed: " + ex.getStatusCode());
		} catch (Exception ex) {
			log.warn("Inventory call failed: orderId={}", orderId, ex);
			return failStock(order, "Inventory call failed");
		}

		try {
			var payResp = paymentClient.createPayment(new PaymentCreateRequest(orderId, order.getTotalAmount()));
			if (payResp != null && "SUCCEEDED".equalsIgnoreCase(payResp.status())) {
				order.setStatus(OrderStatus.CONFIRMED);
				log.info("Order confirmed: orderId={}, total={}", orderId, order.getTotalAmount());
				sqsEventPublisher.publish(
						ordersQueueUrl,
						new OrderConfirmedEvent(UUID.randomUUID(), Instant.now(), orderId, order.getTotalAmount())
				);
				return order;
			}

			log.warn("Payment failed: orderId={}, releasing inventory", orderId);
			inventoryClient.release(orderId);
			order.setStatus(OrderStatus.PAYMENT_FAILED);
			sqsEventPublisher.publish(
					ordersQueueUrl,
					new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), orderId, "Payment failed")
			);
			return order;
		} catch (RestClientResponseException ex) {
			log.warn("Payment call failed: orderId={}, status={}, releasing inventory", orderId, ex.getStatusCode());
			inventoryClient.release(orderId);
			order.setStatus(OrderStatus.PAYMENT_FAILED);
			sqsEventPublisher.publish(
					ordersQueueUrl,
					new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), orderId, "Payment call failed: " + ex.getStatusCode())
			);
			return order;
		}
	}

	@Transactional
	public OrderEntity cancel(UUID orderId, String username) {
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new OrderNotFoundException(orderId));
		verifyOwnership(order, username);

		log.info("Cancelling order: orderId={}, currentStatus={}, user={}", orderId, order.getStatus(), username);

		return switch (order.getStatus()) {
			case PLACED -> {
				order.setStatus(OrderStatus.CANCELLED);
				publishCancelled(orderId, "Cancelled by user");
				log.info("Order cancelled (was PLACED): orderId={}", orderId);
				yield order;
			}
			case CONFIRMED -> {
				try {
					inventoryClient.release(orderId);
					log.info("Inventory released for cancelled order: orderId={}", orderId);
				} catch (Exception ex) {
					log.warn("Best-effort inventory release failed for orderId={}: {}", orderId, ex.getMessage());
				}
				order.setStatus(OrderStatus.CANCELLED);
				publishCancelled(orderId, "Cancelled by user (stock released)");
				yield order;
			}
			case CANCELLED -> throw new IllegalStateException("Order is already cancelled");
			default -> throw new IllegalStateException(
					"Order in status " + order.getStatus() + " cannot be cancelled");
		};
	}

	@Transactional(readOnly = true)
	public OrderEntity get(UUID id) {
		return orderRepository.findById(id)
				.orElseThrow(() -> new OrderNotFoundException(id));
	}

	@Transactional(readOnly = true)
	public List<OrderEntity> listAll() {
		return orderRepository.findAllByOrderByCreatedAtDesc();
	}

	@Transactional(readOnly = true)
	public List<OrderEntity> listByUser(String username) {
		return orderRepository.findByCreatedByOrderByCreatedAtDesc(username);
	}

	@Transactional
	public void deleteAllByUser(String username) {
		orderRepository.deleteByCreatedBy(username);
	}

	private void publishCancelled(UUID orderId, String reason) {
		sqsEventPublisher.publish(
				ordersQueueUrl,
				new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), orderId, reason)
		);
	}

	private OrderEntity failStock(OrderEntity order, String reason) {
		order.setStatus(OrderStatus.STOCK_FAILED);
		sqsEventPublisher.publish(
				ordersQueueUrl,
				new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), order.getId(), reason)
		);
		return order;
	}

	private void verifyOwnership(OrderEntity order, String username) {
		if (!order.getCreatedBy().equals(username)) {
			log.warn("Access denied: user={} attempted to modify orderId={} owned by {}",
					username, order.getId(), order.getCreatedBy());
			throw new OrderAccessDeniedException(order.getId());
		}
	}
}

