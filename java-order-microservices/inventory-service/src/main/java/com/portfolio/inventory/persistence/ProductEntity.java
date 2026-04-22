package com.portfolio.inventory.persistence;

import java.math.BigDecimal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "products")
public class ProductEntity {
	@Id
	@Column(nullable = false)
	private String sku;

	@Column(nullable = false)
	private String name;

	@Column(name = "unit_price", nullable = false, precision = 12, scale = 2)
	private BigDecimal unitPrice;

	protected ProductEntity() {}

	public ProductEntity(String sku, String name, BigDecimal unitPrice) {
		this.sku = sku;
		this.name = name;
		this.unitPrice = unitPrice;
	}

	public String getSku() {
		return sku;
	}

	public String getName() {
		return name;
	}

	public BigDecimal getUnitPrice() {
		return unitPrice;
	}
}

