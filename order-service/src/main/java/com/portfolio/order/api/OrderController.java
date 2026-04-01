package com.portfolio.order.api;

import java.util.UUID;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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
	public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
		var order = orderService.create(request);
		return ResponseEntity.ok(new OrderResponse(order.getId(), order.getStatus().name(), order.getTotalAmount()));
	}

	@PostMapping("/{id}/confirm")
	public ResponseEntity<OrderResponse> confirm(@PathVariable UUID id) {
		var order = orderService.confirm(id);
		return ResponseEntity.ok(new OrderResponse(order.getId(), order.getStatus().name(), order.getTotalAmount()));
	}

	@PostMapping("/{id}/cancel")
	public ResponseEntity<OrderResponse> cancel(@PathVariable UUID id) {
		var order = orderService.cancel(id);
		return ResponseEntity.ok(new OrderResponse(order.getId(), order.getStatus().name(), order.getTotalAmount()));
	}

	@GetMapping("/{id}")
	public ResponseEntity<OrderResponse> get(@PathVariable UUID id) {
		var order = orderService.get(id);
		return ResponseEntity.ok(new OrderResponse(order.getId(), order.getStatus().name(), order.getTotalAmount()));
	}
}

