package com.portfolio.events.payment;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

public record PaymentFailedEvent(
		UUID eventId,
		Instant occurredAt,
		UUID orderId,
		BigDecimal amount,
		String reason
) {}

