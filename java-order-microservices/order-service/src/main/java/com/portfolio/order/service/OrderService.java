package com.portfolio.order.service;

import java.util.List;
import java.util.UUID;

import org.springframework.stereotype.Service;
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
import com.portfolio.order.persistence.OrderEntity;
import com.portfolio.order.persistence.OrderRepository;

@Service
public class OrderService {
	private static final Logger log = LoggerFactory.getLogger(OrderService.class);

	private final OrderRepository orderRepository;
	private final InventoryClient inventoryClient;
	private final PaymentClient paymentClient;
	private final OrderTransactionalWriter transactionalWriter;

	public OrderService(
			OrderRepository orderRepository,
			InventoryClient inventoryClient,
			PaymentClient paymentClient,
			OrderTransactionalWriter transactionalWriter
	) {
		this.orderRepository = orderRepository;
		this.inventoryClient = inventoryClient;
		this.paymentClient = paymentClient;
		this.transactionalWriter = transactionalWriter;
	}

	/**
	 * Creates a new order. Price lookup happens before the transaction opens
	 * so that the HTTP call to inventory-service does not hold a DB connection.
	 */
	public OrderEntity create(CreateOrderRequest request, String username) {
		var skus = request.items().stream().map(i -> i.sku()).toList();
		var prices = inventoryClient.fetchPrices(skus);

		log.info("Creating order for user={} with {} item(s)", username, request.items().size());
		return transactionalWriter.createTransactional(request, username, prices);
	}

	/**
	 * Confirms an order by reserving stock and processing payment.
	 * All HTTP calls happen outside the transaction to preserve DB connections.
	 * Only a short transaction opens to update status after successful calls.
	 */
	public OrderEntity confirm(UUID orderId, String username) {
		// Load order outside transaction
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new OrderNotFoundException(orderId));
		verifyOwnership(order, username);

		if (order.getStatus() != OrderStatus.PLACED) {
			log.debug("Confirm ignored: orderId={} already in status {}", orderId, order.getStatus());
			return order;
		}

		log.info("Confirming order: orderId={}, user={}", orderId, username);

		// Step 1: Reserve stock (HTTP call, outside transaction)
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
				transactionalWriter.failStock(order, reserveResp == null ? "Inventory error" : reserveResp.message());
				return order;
			}
		} catch (RestClientResponseException ex) {
			log.warn("Inventory call failed: orderId={}, status={}", orderId, ex.getStatusCode());
			transactionalWriter.failStock(order, "Inventory call failed: " + ex.getStatusCode());
			return order;
		} catch (Exception ex) {
			log.warn("Inventory call failed: orderId={}", orderId, ex);
			transactionalWriter.failStock(order, "Inventory call failed");
			return order;
		}

		// Step 2: Process payment (HTTP call, outside transaction)
		try {
			var payResp = paymentClient.createPayment(new PaymentCreateRequest(orderId, order.getTotalAmount()));
			if (payResp != null && "SUCCEEDED".equalsIgnoreCase(payResp.status())) {
				// Payment succeeded: update status in short transaction
				transactionalWriter.confirmOrder(order);
				return order;
			}

			// Payment failed: release inventory and mark order as payment failed
			log.warn("Payment failed: orderId={}, releasing inventory", orderId);
			inventoryClient.release(orderId);
			transactionalWriter.failPayment(order, "Payment failed");
			return order;
		} catch (RestClientResponseException ex) {
			log.warn("Payment call failed: orderId={}, status={}, releasing inventory", orderId, ex.getStatusCode());
			inventoryClient.release(orderId);
			transactionalWriter.failPayment(order, "Payment call failed: " + ex.getStatusCode());
			return order;
		}
	}

	/**
	 * Cancels an order. For CONFIRMED orders, releases inventory and refunds payment outside of transaction.
	 * Status update happens in a short transaction.
	 */
	public OrderEntity cancel(UUID orderId, String username) {
		var order = orderRepository.findById(orderId)
				.orElseThrow(() -> new OrderNotFoundException(orderId));
		verifyOwnership(order, username);

		log.info("Cancelling order: orderId={}, currentStatus={}, user={}", orderId, order.getStatus(), username);

		return switch (order.getStatus()) {
			case PLACED -> {
				transactionalWriter.cancelPlaced(order);
				log.info("Order cancelled (was PLACED): orderId={}", orderId);
				yield order;
			}
			case CONFIRMED -> {
				// Release inventory and refund payment outside transaction (best-effort)
				try {
					inventoryClient.release(orderId);
					log.info("Inventory released for cancelled order: orderId={}", orderId);
				} catch (Exception ex) {
					log.warn("Best-effort inventory release failed for orderId={}: {}", orderId, ex.getMessage());
				}

				try {
					var refundResp = paymentClient.refundPayment(
							new com.portfolio.order.clients.PaymentRefundRequest(orderId, order.getTotalAmount())
					);
					if (refundResp != null && "REFUNDED".equalsIgnoreCase(refundResp.status())) {
						log.info("Payment refunded for cancelled order: orderId={}", orderId);
					} else {
						log.warn("Payment refund may have failed for orderId={}: {}", orderId,
								refundResp == null ? "No response" : refundResp.message());
					}
				} catch (Exception ex) {
					log.warn("Best-effort payment refund failed for orderId={}: {}", orderId, ex.getMessage());
				}

				// Update status in transaction
				transactionalWriter.cancelConfirmed(order);
				yield order;
			}
			case CANCELLED -> throw new com.portfolio.order.api.OrderStateConflictException(
					orderId, OrderStatus.CANCELLED, "cancel");
			default -> throw new com.portfolio.order.api.OrderStateConflictException(
					orderId, order.getStatus(), "cancel");
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

	public void deleteAllByUser(String username) {
		transactionalWriter.deleteAllByUser(username);
	}

	private void verifyOwnership(OrderEntity order, String username) {
		if (!order.getCreatedBy().equals(username)) {
			log.warn("Access denied: user={} attempted to modify orderId={} owned by {}",
					username, order.getId(), order.getCreatedBy());
			throw new OrderAccessDeniedException(order.getId());
		}
	}
}

