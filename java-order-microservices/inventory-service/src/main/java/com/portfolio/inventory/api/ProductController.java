package com.portfolio.inventory.api;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.inventory.persistence.ProductEntity;
import com.portfolio.inventory.persistence.ProductRepository;

@RestController
@RequestMapping("/products")
public class ProductController {
	private final ProductRepository productRepository;

	public ProductController(ProductRepository productRepository) {
		this.productRepository = productRepository;
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

	public record ProductResponse(String sku, String name, BigDecimal unitPrice) {}
}
