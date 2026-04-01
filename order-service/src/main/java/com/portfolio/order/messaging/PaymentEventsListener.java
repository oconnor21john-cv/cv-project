package com.portfolio.order.messaging;

import org.springframework.kafka.annotation.KafkaHandler;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import com.portfolio.events.payment.PaymentFailedEvent;
import com.portfolio.events.payment.PaymentSucceededEvent;
import com.portfolio.order.persistence.OrderRepository;

@Component
@KafkaListener(topics = "${app.kafka.topic.payments}", groupId = "order-service")
public class PaymentEventsListener {
	private final OrderRepository orderRepository;

	public PaymentEventsListener(OrderRepository orderRepository) {
		this.orderRepository = orderRepository;
	}

	@KafkaHandler
	@Transactional
	public void handle(PaymentSucceededEvent event) {
		orderRepository.findById(event.orderId()).ifPresent(order -> order.addHistory("PAYMENT_SUCCEEDED"));
	}

	@KafkaHandler
	@Transactional
	public void handle(PaymentFailedEvent event) {
		orderRepository.findById(event.orderId())
				.ifPresent(order -> order.addHistory("PAYMENT_FAILED: " + event.reason()));
	}

	@KafkaHandler(isDefault = true)
	public void handleDefault(Object unknown) {
		// ignore
	}
}

