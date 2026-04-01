package com.portfolio.payment.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.portfolio.payment.domain.PaymentStatus;
import com.portfolio.payment.persistence.PaymentEntity;
import com.portfolio.payment.persistence.PaymentRepository;
import com.portfolio.events.payment.PaymentFailedEvent;
import com.portfolio.events.payment.PaymentSucceededEvent;

@Service
public class PaymentService {
	private final PaymentRepository paymentRepository;
	private final KafkaTemplate<String, Object> kafkaTemplate;
	private final String paymentsTopic;

	public PaymentService(
			PaymentRepository paymentRepository,
			KafkaTemplate<String, Object> kafkaTemplate,
			@Value("${app.kafka.topic.payments}") String paymentsTopic
	) {
		this.paymentRepository = paymentRepository;
		this.kafkaTemplate = kafkaTemplate;
		this.paymentsTopic = paymentsTopic;
	}

	@Transactional
	public Result createOrGet(UUID orderId, BigDecimal amount) {
		var existing = paymentRepository.findByOrderId(orderId);
		if (existing.isPresent()) {
			var p = existing.get();
			return switch (p.getStatus()) {
				case SUCCEEDED -> Result.succeeded("Already paid");
				case FAILED -> Result.failed("Already failed");
			};
		}

		var status = decide(amount);
		var payment = new PaymentEntity(orderId, amount, status);
		paymentRepository.save(payment);

		if (status == PaymentStatus.SUCCEEDED) {
			kafkaTemplate.send(
					paymentsTopic,
					orderId.toString(),
					new PaymentSucceededEvent(UUID.randomUUID(), Instant.now(), orderId, amount)
			);
			return Result.succeeded("Payment succeeded");
		}

		var reason = "Mock decline (amount too high)";
		kafkaTemplate.send(
				paymentsTopic,
				orderId.toString(),
				new PaymentFailedEvent(UUID.randomUUID(), Instant.now(), orderId, amount, reason)
		);
		return Result.failed(reason);
	}

	private PaymentStatus decide(BigDecimal amount) {
		if (amount.compareTo(new BigDecimal("1000.00")) > 0) {
			return PaymentStatus.FAILED;
		}
		return PaymentStatus.SUCCEEDED;
	}

	public record Result(boolean succeeded, String message) {
		public static Result succeeded(String msg) { return new Result(true, msg); }
		public static Result failed(String msg) { return new Result(false, msg); }
	}
}

