package com.portfolio.payment.persistence;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

import com.portfolio.payment.domain.PaymentStatus;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "payments")
public class PaymentEntity {
	@Id
	@Column(nullable = false)
	private UUID id;

	@Column(name = "order_id", nullable = false, unique = true)
	private UUID orderId;

	@Column(nullable = false, precision = 12, scale = 2)
	private BigDecimal amount;

	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private PaymentStatus status;

	@Column(name = "created_at", nullable = false)
	private Instant createdAt;

	protected PaymentEntity() {}

	public PaymentEntity(UUID orderId, BigDecimal amount, PaymentStatus status) {
		this.id = UUID.randomUUID();
		this.orderId = orderId;
		this.amount = amount;
		this.status = status;
		this.createdAt = Instant.now();
	}

	public UUID getId() {
		return id;
	}

	public UUID getOrderId() {
		return orderId;
	}

	public BigDecimal getAmount() {
		return amount;
	}

	public PaymentStatus getStatus() {
		return status;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}
}

