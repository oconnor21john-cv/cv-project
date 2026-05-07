package com.portfolio.order.api;

import java.security.Principal;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.order.clients.InventoryClient;
import com.portfolio.order.persistence.OrderEntity;
import com.portfolio.order.service.OrderService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/orders")
public class OrderController {
	private final OrderService orderService;
	private final InventoryClient inventoryClient;

	public OrderController(OrderService orderService, InventoryClient inventoryClient) {
		this.orderService = orderService;
		this.inventoryClient = inventoryClient;
	}

	@PostMapping
	public ResponseEntity<OrderResponse> create(
			@Valid @RequestBody CreateOrderRequest request,
			Principal principal
	) {
		var order = orderService.create(request, principal.getName());
		// Fetch stock for items in newly created order
		var skus = order.getItems().stream().map(item -> item.getSku()).toList();
		Map<String, Integer> stockMap = skus.isEmpty() ? Map.of() : inventoryClient.fetchStock(skus);
		return ResponseEntity.ok(toResponse(order, stockMap));
	}

	@GetMapping
	public ResponseEntity<List<OrderResponse>> list(Authentication auth) {
		var username = auth.getName();
		var isAdmin = auth.getAuthorities().stream()
				.map(GrantedAuthority::getAuthority)
				.anyMatch(a -> a.equals("ROLE_ADMIN"));

		var orders = isAdmin
				? orderService.listAll()
				: orderService.listByUser(username);

		// Fetch stock for all distinct SKUs in the result set
		var allSkus = orders.stream()
				.flatMap(o -> o.getItems().stream())
				.map(item -> item.getSku())
				.collect(Collectors.toSet());

		Map<String, Integer> stockMap = allSkus.isEmpty() ? Map.of() : inventoryClient.fetchStock(allSkus.stream().toList());

		return ResponseEntity.ok(orders.stream()
				.map(order -> toResponse(order, stockMap))
				.toList());
	}

	@PostMapping("/{id}/confirm")
	public ResponseEntity<OrderResponse> confirm(@PathVariable UUID id, Principal principal) {
		var order = orderService.confirm(id, principal.getName());
		// Fetch stock for items in confirmed order
		var skus = order.getItems().stream().map(item -> item.getSku()).toList();
		Map<String, Integer> stockMap = skus.isEmpty() ? Map.of() : inventoryClient.fetchStock(skus);
		return ResponseEntity.ok(toResponse(order, stockMap));
	}

	@PostMapping("/{id}/cancel")
	public ResponseEntity<OrderResponse> cancel(@PathVariable UUID id, Principal principal) {
		var order = orderService.cancel(id, principal.getName());
		// Fetch stock for items in cancelled order
		var skus = order.getItems().stream().map(item -> item.getSku()).toList();
		Map<String, Integer> stockMap = skus.isEmpty() ? Map.of() : inventoryClient.fetchStock(skus);
		return ResponseEntity.ok(toResponse(order, stockMap));
	}

	@GetMapping("/{id}")
	public ResponseEntity<OrderResponse> get(@PathVariable UUID id) {
		var order = orderService.get(id);

		// Fetch stock for all SKUs in this order
		var skus = order.getItems().stream()
				.map(item -> item.getSku())
				.toList();

		Map<String, Integer> stockMap = skus.isEmpty() ? Map.of() : inventoryClient.fetchStock(skus);

		return ResponseEntity.ok(toResponse(order, stockMap));
	}

	/**
	 * Convert OrderEntity to OrderResponse, merging in current stock levels.
	 *
	 * @param order The order entity
	 * @param stockMap Stock data (SKU → remaining quantity). Items not in map get null remainingStock.
	 */
	private OrderResponse toResponse(OrderEntity order, Map<String, Integer> stockMap) {
		var items = order.getItems().stream()
				.map(i -> new OrderResponse.Item(
						i.getSku(),
						i.getQuantity(),
						i.getUnitPrice(),
						stockMap.get(i.getSku())  // Nullable: null if unknown, 0 if out of stock, >0 if available
				))
				.toList();
		return new OrderResponse(
				order.getId(),
				order.getStatus().name(),
				order.getTotalAmount(),
				order.getCreatedBy(),
				order.getCreatedAt(),
				items
		);
	}
}
