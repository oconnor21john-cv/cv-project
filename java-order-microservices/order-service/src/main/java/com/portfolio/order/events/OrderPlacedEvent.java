package com.portfolio.order.events;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.UUID;

public record OrderPlacedEvent(
		UUID eventId,
		Instant occurredAt,
		UUID orderId,
		BigDecimal totalAmount,
		List<Item> items
) {
	public record Item(String sku, int quantity, BigDecimal unitPrice) {}
}

