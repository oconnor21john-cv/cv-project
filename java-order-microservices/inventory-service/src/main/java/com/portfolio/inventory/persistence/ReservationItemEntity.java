package com.portfolio.inventory.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "reservation_items")
public class ReservationItemEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private long id;

	@ManyToOne(optional = false)
	@JoinColumn(name = "order_id", nullable = false)
	private ReservationEntity reservation;

	@Column(nullable = false)
	private String sku;

	@Column(nullable = false)
	private int quantity;

	protected ReservationItemEntity() {}

	public ReservationItemEntity(ReservationEntity reservation, String sku, int quantity) {
		this.reservation = reservation;
		this.sku = sku;
		this.quantity = quantity;
	}

	public long getId() {
		return id;
	}

	public String getSku() {
		return sku;
	}

	public int getQuantity() {
		return quantity;
	}
}

