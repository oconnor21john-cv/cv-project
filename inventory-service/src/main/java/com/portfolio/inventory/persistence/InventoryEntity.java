package com.portfolio.inventory.persistence;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

@Entity
@Table(name = "inventory")
public class InventoryEntity {
	@Id
	@Column(nullable = false)
	private String sku;

	@Column(name = "on_hand", nullable = false)
	private int onHand;

	@Column(nullable = false)
	private int reserved;

	@Version
	@Column(nullable = false)
	private long version;

	protected InventoryEntity() {}

	public InventoryEntity(String sku, int onHand, int reserved) {
		this.sku = sku;
		this.onHand = onHand;
		this.reserved = reserved;
	}

	public String getSku() {
		return sku;
	}

	public int getOnHand() {
		return onHand;
	}

	public int getReserved() {
		return reserved;
	}

	public int getAvailable() {
		return onHand - reserved;
	}

	public void reserve(int quantity) {
		if (quantity <= 0) {
			throw new IllegalArgumentException("quantity must be positive");
		}
		this.reserved += quantity;
	}

	public void release(int quantity) {
		if (quantity <= 0) {
			throw new IllegalArgumentException("quantity must be positive");
		}
		this.reserved -= quantity;
		if (this.reserved < 0) {
			this.reserved = 0;
		}
	}
}

