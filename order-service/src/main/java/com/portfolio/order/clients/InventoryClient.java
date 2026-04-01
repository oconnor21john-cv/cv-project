package com.portfolio.order.clients;

import java.util.UUID;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class InventoryClient {
	private final RestClient inventoryRestClient;

	public InventoryClient(@Qualifier("inventoryRestClient") RestClient inventoryRestClient) {
		this.inventoryRestClient = inventoryRestClient;
	}

	public InventoryReserveResponse reserve(InventoryReserveRequest request) {
		return inventoryRestClient.post()
				.uri("/reservations")
				.contentType(MediaType.APPLICATION_JSON)
				.body(request)
				.retrieve()
				.body(InventoryReserveResponse.class);
	}

	public void release(UUID orderId) {
		inventoryRestClient.delete()
				.uri("/reservations/{orderId}", orderId)
				.retrieve()
				.toBodilessEntity();
	}
}

