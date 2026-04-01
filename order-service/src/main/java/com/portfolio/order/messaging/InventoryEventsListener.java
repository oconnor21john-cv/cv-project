package com.portfolio.order.messaging;

import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.portfolio.events.inventory.StockReservationFailedEvent;
import com.portfolio.events.inventory.StockReservedEvent;
import com.portfolio.order.persistence.OrderRepository;

@Component
@KafkaListener(topics = "${app.kafka.topic.inventory}", groupId = "order-service")
public class InventoryEventsListener {
	private final OrderRepository orderRepository;

	public InventoryEventsListener(OrderRepository orderRepository) {
		this.orderRepository = orderRepository;
	}

	@KafkaHandler
	@Transactional
	public void handle(StockReservedEvent event) {
		orderRepository.findById(event.orderId()).ifPresent(order -> order.addHistory("INVENTORY_RESERVED"));
	}

	@KafkaHandler
	@Transactional
	public void handle(StockReservationFailedEvent event) {
		orderRepository.findById(event.orderId())
				.ifPresent(order -> order.addHistory("INVENTORY_FAILED: " + event.reason()));
	}

	@KafkaHandler(isDefault = true)
	public void handleDefault(Object unknown) {
		// ignore
	}
}

