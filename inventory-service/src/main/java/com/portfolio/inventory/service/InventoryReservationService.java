package com.portfolio.inventory.service;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.portfolio.inventory.api.ReserveStockRequest;
import com.portfolio.inventory.domain.ReservationStatus;
import com.portfolio.inventory.persistence.InventoryEntity;
import com.portfolio.inventory.persistence.InventoryRepository;
import com.portfolio.inventory.persistence.ReservationEntity;
import com.portfolio.inventory.persistence.ReservationRepository;
import com.portfolio.events.inventory.StockReservationFailedEvent;
import com.portfolio.events.inventory.StockReservedEvent;

@Service
public class InventoryReservationService {
	private final InventoryRepository inventoryRepository;
	private final ReservationRepository reservationRepository;
	private final KafkaTemplate<String, Object> kafkaTemplate;
	private final String inventoryTopic;

	public InventoryReservationService(
			InventoryRepository inventoryRepository,
			ReservationRepository reservationRepository,
			KafkaTemplate<String, Object> kafkaTemplate,
			@Value("${app.kafka.topic.inventory}") String inventoryTopic
	) {
		this.inventoryRepository = inventoryRepository;
		this.reservationRepository = reservationRepository;
		this.kafkaTemplate = kafkaTemplate;
		this.inventoryTopic = inventoryTopic;
	}

	@Transactional
	public Result reserve(ReserveStockRequest request) {
		var existing = reservationRepository.findWithItemsByOrderId(request.orderId());
		if (existing.isPresent()) {
			return switch (existing.get().getStatus()) {
				case RESERVED -> Result.reserved("Already reserved");
				case RELEASED -> Result.failed("Already released");
				case FAILED -> Result.failed("Already failed");
			};
		}

		for (var item : request.items()) {
			var inv = inventoryRepository.findBySkuForUpdate(item.sku())
					.orElse(null);
			if (inv == null) {
				return failAndPublish(request.orderId(), "Unknown SKU: " + item.sku(), request);
			}
			if (inv.getAvailable() < item.quantity()) {
				return failAndPublish(request.orderId(), "Insufficient stock for " + item.sku(), request);
			}
		}

		for (var item : request.items()) {
			InventoryEntity inv = inventoryRepository.findBySkuForUpdate(item.sku()).orElseThrow();
			inv.reserve(item.quantity());
		}

		var reservation = new ReservationEntity(request.orderId(), ReservationStatus.RESERVED);
		for (var item : request.items()) {
			reservation.addItem(item.sku(), item.quantity());
		}
		reservationRepository.save(reservation);

		var event = new StockReservedEvent(
				UUID.randomUUID(),
				Instant.now(),
				request.orderId(),
				request.items().stream()
						.map(i -> new StockReservedEvent.Item(i.sku(), i.quantity()))
						.toList()
		);
		kafkaTemplate.send(inventoryTopic, request.orderId().toString(), event);

		return Result.reserved("Reserved");
	}

	@Transactional
	public Result release(UUID orderId) {
		var existing = reservationRepository.findWithItemsByOrderId(orderId);
		if (existing.isEmpty()) {
			return Result.reserved("No reservation found (noop)");
		}

		var reservation = existing.get();
		if (reservation.getStatus() != ReservationStatus.RESERVED) {
			return Result.reserved("Reservation not in RESERVED state (noop)");
		}

		for (var item : reservation.getItems()) {
			var inv = inventoryRepository.findBySkuForUpdate(item.getSku()).orElse(null);
			if (inv != null) {
				inv.release(item.getQuantity());
			}
		}
		reservation.setStatus(ReservationStatus.RELEASED);

		return Result.reserved("Released");
	}

	private Result failAndPublish(UUID orderId, String reason, ReserveStockRequest request) {
		var reservation = new ReservationEntity(orderId, ReservationStatus.FAILED);
		for (var item : request.items()) {
			reservation.addItem(item.sku(), item.quantity());
		}
		reservationRepository.save(reservation);

		var event = new StockReservationFailedEvent(
				UUID.randomUUID(),
				Instant.now(),
				orderId,
				reason,
				request.items().stream()
						.map(i -> new StockReservationFailedEvent.Item(i.sku(), i.quantity()))
						.toList()
		);
		kafkaTemplate.send(inventoryTopic, orderId.toString(), event);

		return Result.failed(reason);
	}

	public record Result(boolean reserved, String message) {
		public static Result reserved(String msg) { return new Result(true, msg); }
		public static Result failed(String msg) { return new Result(false, msg); }
	}
}

