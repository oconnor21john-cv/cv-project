package com.portfolio.order.api;

import java.util.List;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;

public record CreateOrderRequest(
		@NotEmpty @Valid List<CreateOrderRequestItem> items
) {}

