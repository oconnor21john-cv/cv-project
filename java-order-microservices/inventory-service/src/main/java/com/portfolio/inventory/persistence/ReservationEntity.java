package com.portfolio.inventory.persistence;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import com.portfolio.inventory.domain.ReservationStatus;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "reservations")
public class ReservationEntity {
	@Id
	@Column(name = "order_id", nullable = false)
	private UUID orderId;

	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private ReservationStatus status;

	@Column(name = "created_at", nullable = false)
	private Instant createdAt;

	@OneToMany(mappedBy = "reservation", cascade = CascadeType.ALL, orphanRemoval = true)
	private List<ReservationItemEntity> items = new ArrayList<>();

	protected ReservationEntity() {}

	public ReservationEntity(UUID orderId, ReservationStatus status) {
		this.orderId = orderId;
		this.status = status;
		this.createdAt = Instant.now();
	}

	public UUID getOrderId() {
		return orderId;
	}

	public ReservationStatus getStatus() {
		return status;
	}

	public void setStatus(ReservationStatus status) {
		this.status = status;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}

	public List<ReservationItemEntity> getItems() {
		return items;
	}

	public void addItem(String sku, int quantity) {
		this.items.add(new ReservationItemEntity(this, sku, quantity));
	}
}

