package com.portfolio.order.api;

import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.order.clients.InventoryClient;

/**
 * Catalog endpoints for the web UI. Proxies inventory-service so the
 * frontend never has to know inventory-service exists or hold a second
 * base URL. Auth is enforced by the JWT chain in SecurityConfig.
 */
@RestController
@RequestMapping("/catalog")
public class CatalogController {
	private final InventoryClient inventoryClient;

	public CatalogController(InventoryClient inventoryClient) {
		this.inventoryClient = inventoryClient;
	}

	/**
	 * Live stock for the given SKUs.
	 *
	 * Returns: SKU → available quantity (clamped at 0).
	 * Unknown SKUs are omitted from the map.
	 * Returns an empty map if inventory-service is unavailable
	 * (circuit-breaker fallback in InventoryClient).
	 */
	@GetMapping("/stock")
	public Map<String, Integer> stock(@RequestParam List<String> skus) {
		return inventoryClient.fetchStock(skus);
	}
}
