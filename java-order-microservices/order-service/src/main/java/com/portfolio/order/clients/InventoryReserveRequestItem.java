package com.portfolio.order.clients;

public record InventoryReserveRequestItem(
		String sku,
		int quantity
) {}

