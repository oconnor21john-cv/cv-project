package com.portfolio.inventory.api;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.inventory.persistence.InventoryRepository;
import com.portfolio.inventory.persistence.ProductEntity;
import com.portfolio.inventory.persistence.ProductRepository;

@RestController
@RequestMapping("/products")
public class ProductController {
	private final ProductRepository productRepository;
	private final InventoryRepository inventoryRepository;

	public ProductController(ProductRepository productRepository, InventoryRepository inventoryRepository) {
		this.productRepository = productRepository;
		this.inventoryRepository = inventoryRepository;
	}

	@GetMapping
	public List<ProductResponse> listAll() {
		return productRepository.findAll().stream()
				.map(p -> new ProductResponse(p.getSku(), p.getName(), p.getUnitPrice()))
				.toList();
	}

	@GetMapping("/prices")
	public Map<String, BigDecimal> prices(@RequestParam List<String> skus) {
		return productRepository.findBySkuIn(skus).stream()
				.collect(Collectors.toMap(ProductEntity::getSku, ProductEntity::getUnitPrice));
	}

	/**
	 * Get current available stock (on-hand minus reserved) for given SKUs.
	 *
	 * @param skus List of product SKUs
	 * @return Map of SKU to remaining quantity (clamped at 0)
	 *         Unknown SKUs are omitted from the map
	 */
	@GetMapping("/stock")
	public Map<String, Integer> stock(@RequestParam List<String> skus) {
		return inventoryRepository.findBySkuIn(skus).stream()
				.collect(Collectors.toMap(
						inv -> inv.getSku(),
						inv -> Math.max(0, inv.getAvailable())  // Clamp at 0
				));
	}

	public record ProductResponse(String sku, String name, BigDecimal unitPrice) {}
}
