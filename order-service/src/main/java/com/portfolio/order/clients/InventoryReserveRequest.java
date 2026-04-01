package com.portfolio.order.clients;

import java.util.List;
import java.util.UUID;

public record InventoryReserveRequest(
		UUID orderId,
		List<InventoryReserveRequestItem> items
) {}

