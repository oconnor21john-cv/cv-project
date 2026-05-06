package com.portfolio.order.api;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

public record OrderResponse(
		UUID id,
		String status,
		BigDecimal totalAmount,
		String createdBy,
		Instant createdAt,
		List<Item> items
) {
	/**
	 * Item with optional remainingStock.
	 * If null: stock lookup failed or SKU was deleted.
	 * If 0: out of stock.
	 * If > 0: available quantity.
	 */
	public record Item(String sku, int quantity, BigDecimal unitPrice, Integer remainingStock) {}
}
