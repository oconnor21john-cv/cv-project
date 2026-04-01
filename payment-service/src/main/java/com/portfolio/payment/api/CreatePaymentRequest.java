package com.portfolio.payment.api;

import java.math.BigDecimal;
import java.util.UUID;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;

public record CreatePaymentRequest(
		@NotNull UUID orderId,
		@NotNull @DecimalMin("0.00") BigDecimal amount
) {}

