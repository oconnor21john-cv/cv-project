package com.portfolio.inventory.api;

import java.util.UUID;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.inventory.service.InventoryReservationService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/reservations")
public class ReservationController {
	private final InventoryReservationService reservationService;

	public ReservationController(InventoryReservationService reservationService) {
		this.reservationService = reservationService;
	}

	@PostMapping
	public ResponseEntity<ReserveStockResponse> reserve(@Valid @RequestBody ReserveStockRequest request) {
		var result = reservationService.reserve(request);
		if (result.reserved()) {
			return ResponseEntity.ok(new ReserveStockResponse("RESERVED", result.message()));
		}
		return ResponseEntity.badRequest().body(new ReserveStockResponse("FAILED", result.message()));
	}

	@DeleteMapping("/{orderId}")
	public ResponseEntity<ReserveStockResponse> release(@PathVariable UUID orderId) {
		var result = reservationService.release(orderId);
		return ResponseEntity.ok(new ReserveStockResponse("RELEASED", result.message()));
	}
}

