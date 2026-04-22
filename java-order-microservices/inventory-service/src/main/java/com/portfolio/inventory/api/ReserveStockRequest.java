package com.portfolio.inventory.api;

import java.util.List;
import java.util.UUID;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

public record ReserveStockRequest(
		@NotNull UUID orderId,
		@NotEmpty @Valid List<ReserveStockRequestItem> items
) {}

