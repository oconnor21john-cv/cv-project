package com.portfolio.events.inventory;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

public record StockReservationFailedEvent(
		UUID eventId,
		Instant occurredAt,
		UUID orderId,
		String reason,
		List<Item> items
) {
	public record Item(String sku, int quantity) {}
}

