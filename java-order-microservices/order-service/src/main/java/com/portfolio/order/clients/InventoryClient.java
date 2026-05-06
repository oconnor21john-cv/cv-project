package com.portfolio.order.clients;

import java.math.BigDecimal;
import java.util.Map;
import java.util.UUID;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class InventoryClient {
	private final RestClient inventoryRestClient;

	public InventoryClient(@Qualifier("inventoryRestClient") RestClient inventoryRestClient) {
		this.inventoryRestClient = inventoryRestClient;
	}

	@CircuitBreaker(name = "inventory")
	public Map<String, BigDecimal> fetchPrices(java.util.List<String> skus) {
		String skuParam = String.join(",", skus);
		return inventoryRestClient.get()
				.uri("/products/prices?skus={skus}", skuParam)
				.retrieve()
				.body(new ParameterizedTypeReference<>() {});
	}

	/**
	 * Fetch current available stock for given SKUs.
	 * Fallback returns empty map if inventory-service is down (caller treats as "unknown").
	 */
	@CircuitBreaker(name = "inventory", fallbackMethod = "stockFallback")
	public Map<String, Integer> fetchStock(java.util.List<String> skus) {
		String skuParam = String.join(",", skus);
		return inventoryRestClient.get()
				.uri("/products/stock?skus={skus}", skuParam)
				.retrieve()
				.body(new ParameterizedTypeReference<>() {});
	}

	// Fallback for fetchStock: return empty map if inventory-service is unavailable
	private Map<String, Integer> stockFallback(java.util.List<String> skus, Throwable throwable) {
		return Map.of();
	}

	@CircuitBreaker(name = "inventory")
	public InventoryReserveResponse reserve(InventoryReserveRequest request) {
		return inventoryRestClient.post()
				.uri("/reservations")
				.contentType(MediaType.APPLICATION_JSON)
				.body(request)
				.retrieve()
				.body(InventoryReserveResponse.class);
	}

	@CircuitBreaker(name = "inventory")
	public void release(UUID orderId) {
		inventoryRestClient.delete()
				.uri("/reservations/{orderId}", orderId)
				.retrieve()
				.toBodilessEntity();
	}
}
