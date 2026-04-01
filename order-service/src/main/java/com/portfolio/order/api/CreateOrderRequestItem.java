package com.portfolio.order.api;

import java.math.BigDecimal;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record CreateOrderRequestItem(
		@NotBlank String sku,
		@Min(1) int quantity,
		@NotNull @DecimalMin("0.00") BigDecimal unitPrice
) {}

