package com.portfolio.order.events;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record OrderConfirmedEvent(
		UUID eventId,
		Instant occurredAt,
		UUID orderId,
		BigDecimal totalAmount
) {}

