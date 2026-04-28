package com.portfolio.order.api;

import java.security.Principal;
import java.util.List;
import java.util.UUID;

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

import com.portfolio.order.persistence.OrderEntity;
import com.portfolio.order.service.OrderService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/orders")
public class OrderController {
	private final OrderService orderService;

	public OrderController(OrderService orderService) {
		this.orderService = orderService;
	}

	@PostMapping
	public ResponseEntity<OrderResponse> create(
			@Valid @RequestBody CreateOrderRequest request,
			Principal principal
	) {
		var order = orderService.create(request, principal.getName());
		return ResponseEntity.ok(toResponse(order));
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

		return ResponseEntity.ok(orders.stream().map(this::toResponse).toList());
	}

	@PostMapping("/{id}/confirm")
	public ResponseEntity<OrderResponse> confirm(@PathVariable UUID id) {
		var order = orderService.confirm(id);
		return ResponseEntity.ok(toResponse(order));
	}

	@PostMapping("/{id}/cancel")
	public ResponseEntity<OrderResponse> cancel(@PathVariable UUID id) {
		var order = orderService.cancel(id);
		return ResponseEntity.ok(toResponse(order));
	}

	@DeleteMapping
	public ResponseEntity<Void> deleteAll(Authentication auth) {
		var username = auth.getName();
		orderService.deleteAllByUser(username);
		return ResponseEntity.noContent().build();
	}

	@GetMapping("/{id}")
	public ResponseEntity<OrderResponse> get(@PathVariable UUID id) {
		var order = orderService.get(id);
		return ResponseEntity.ok(toResponse(order));
	}

	private OrderResponse toResponse(OrderEntity order) {
		var items = order.getItems().stream()
				.map(i -> new OrderResponse.Item(i.getSku(), i.getQuantity(), i.getUnitPrice()))
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
