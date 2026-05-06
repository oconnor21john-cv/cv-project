package com.portfolio.order.clients;

import java.math.BigDecimal;
import java.util.UUID;

public record PaymentRefundRequest(
		UUID orderId,
		BigDecimal amount
) {}
