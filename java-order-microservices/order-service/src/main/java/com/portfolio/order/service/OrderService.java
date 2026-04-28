package com.portfolio.order.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClientResponseException;

import com.portfolio.order.api.CreateOrderRequest;
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

	@Transactional
	public OrderEntity create(CreateOrderRequest request, String username) {
		var orderId = UUID.randomUUID();

		var skus = request.items().stream().map(i -> i.sku()).toList();
		var prices = inventoryClient.fetchPrices(skus);

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

		return order;
	}

	@Transactional
	public OrderEntity confirm(UUID orderId) {
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

		if (order.getStatus() != OrderStatus.PLACED) {
			return order;
		}

		var reserveReq = new InventoryReserveRequest(
				orderId,
				order.getItems().stream()
						.map(i -> new InventoryReserveRequestItem(i.getSku(), i.getQuantity()))
						.toList()
		);

		try {
			var reserveResp = inventoryClient.reserve(reserveReq);
			if (reserveResp == null || !"RESERVED".equalsIgnoreCase(reserveResp.status())) {
				return failStock(order, reserveResp == null ? "Inventory error" : reserveResp.message());
			}
		} catch (RestClientResponseException ex) {
			return failStock(order, "Inventory call failed: " + ex.getStatusCode());
		} catch (Exception ex) {
			return failStock(order, "Inventory call failed");
		}

		try {
			var payResp = paymentClient.createPayment(new PaymentCreateRequest(orderId, order.getTotalAmount()));
			if (payResp != null && "SUCCEEDED".equalsIgnoreCase(payResp.status())) {
				order.setStatus(OrderStatus.CONFIRMED);
				sqsEventPublisher.publish(
						ordersQueueUrl,
						new OrderConfirmedEvent(UUID.randomUUID(), Instant.now(), orderId, order.getTotalAmount())
				);
				return order;
			}

			inventoryClient.release(orderId);
			order.setStatus(OrderStatus.PAYMENT_FAILED);
			sqsEventPublisher.publish(
					ordersQueueUrl,
					new OrderCancelledEvent(UUID.randomUUID(), Instant.now(), orderId, "Payment failed")
			);
			return order;
		} catch (RestClientResponseException ex) {
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
	public OrderEntity cancel(UUID orderId) {
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

		return switch (order.getStatus()) {
			case PLACED -> {
				order.setStatus(OrderStatus.CANCELLED);
				publishCancelled(orderId, "Cancelled by user");
				yield order;
			}
			case CONFIRMED -> {
				try {
					inventoryClient.release(orderId);
				} catch (Exception ignored) {
					// best-effort compensation; can be reconciled asynchronously
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
				.orElseThrow(() -> new IllegalArgumentException("Order not found: " + id));
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
}

