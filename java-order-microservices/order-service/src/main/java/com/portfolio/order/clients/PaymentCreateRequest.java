package com.portfolio.order.clients;

import java.math.BigDecimal;
import java.util.UUID;

public record PaymentCreateRequest(
		UUID orderId,
		BigDecimal amount
) {}

