package com.portfolio.order.api;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public record CreateOrderRequestItem(
		@NotBlank String sku,
		@Min(1) int quantity
) {}
