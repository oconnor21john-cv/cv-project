package com.portfolio.order.persistence;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import com.portfolio.order.domain.OrderStatus;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "orders")
public class OrderEntity {
	@Id
	@Column(nullable = false)
	private UUID id;

	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private OrderStatus status;

	@Column(name = "total_amount", nullable = false, precision = 12, scale = 2)
	private BigDecimal totalAmount;

	@Column(name = "created_at", nullable = false)
	private Instant createdAt;

	@Column(name = "created_by", nullable = false)
	private String createdBy;

	// EAGER because every read path (GET /orders, GET /orders/{id}, confirm,
	// cancel) iterates items immediately after loading the order, and
	// spring.jpa.open-in-view=false means the session closes when the
	// @Transactional method returns. Lazy would throw LazyInitializationException
	// on access in the controller. Items per order are small and bounded, so
	// the cartesian-product concern doesn't apply at this scale.
	@OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
	private List<OrderItemEntity> items = new ArrayList<>();

	// EAGER for the same reason as `items`: setStatus() calls addHistory()
	// which mutates this collection, and confirm/cancel/clear paths do this
	// outside the load transaction. With open-in-view=false the proxy can't
	// initialize lazily and Hibernate throws LazyInitializationException.
	@OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
	private List<OrderStatusHistoryEntity> statusHistory = new ArrayList<>();

	protected OrderEntity() {}

	public OrderEntity(UUID id, BigDecimal totalAmount, String createdBy) {
		this.id = id;
		this.totalAmount = totalAmount;
		this.createdBy = createdBy;
		this.status = OrderStatus.PLACED;
		this.createdAt = Instant.now();
		addHistory(this.status.name());
	}

	public UUID getId() {
		return id;
	}

	public OrderStatus getStatus() {
		return status;
	}

	public void setStatus(OrderStatus status) {
		this.status = status;
		addHistory(status.name());
	}

	public BigDecimal getTotalAmount() {
		return totalAmount;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}

	public String getCreatedBy() {
		return createdBy;
	}

	public List<OrderItemEntity> getItems() {
		return items;
	}

	public List<OrderStatusHistoryEntity> getStatusHistory() {
		return statusHistory;
	}

	public void addItem(String sku, int quantity, BigDecimal unitPrice) {
		this.items.add(new OrderItemEntity(this, sku, quantity, unitPrice));
	}

	public void addHistory(String status) {
		this.statusHistory.add(new OrderStatusHistoryEntity(this, status));
	}
}

