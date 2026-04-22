package com.portfolio.order.persistence;

import java.time.Instant;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "order_status_history")
public class OrderStatusHistoryEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;

	@ManyToOne(optional = false)
	@JoinColumn(name = "order_id", nullable = false)
	private OrderEntity order;

	@Column(nullable = false)
	private String status;

	@Column(name = "occurred_at", nullable = false)
	private Instant occurredAt;

	protected OrderStatusHistoryEntity() {}

	public OrderStatusHistoryEntity(OrderEntity order, String status) {
		this.order = order;
		this.status = status;
		this.occurredAt = Instant.now();
	}

	public long getId() {
		return id;
	}

	public String getStatus() {
		return status;
	}

	public Instant getOccurredAt() {
		return occurredAt;
	}
}

