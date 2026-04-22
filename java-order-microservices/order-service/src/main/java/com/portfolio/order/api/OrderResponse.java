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
	public record Item(String sku, int quantity, BigDecimal unitPrice) {}
}
