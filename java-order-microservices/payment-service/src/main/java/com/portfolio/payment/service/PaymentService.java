package com.portfolio.payment.service;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.portfolio.payment.domain.PaymentStatus;
import com.portfolio.payment.messaging.SqsEventPublisher;
import com.portfolio.payment.persistence.PaymentEntity;
import com.portfolio.payment.persistence.PaymentRepository;
import com.portfolio.events.payment.PaymentFailedEvent;
import com.portfolio.events.payment.PaymentSucceededEvent;

@Service
public class PaymentService {
	private static final Logger log = LoggerFactory.getLogger(PaymentService.class);

	private final PaymentRepository paymentRepository;
	private final SqsEventPublisher sqsEventPublisher;
	private final String paymentsQueueUrl;

	public PaymentService(
			PaymentRepository paymentRepository,
			SqsEventPublisher sqsEventPublisher,
			@Value("${app.sqs.queue.payments.url:}") String paymentsQueueUrl
	) {
		this.paymentRepository = paymentRepository;
		this.sqsEventPublisher = sqsEventPublisher;
		this.paymentsQueueUrl = paymentsQueueUrl;
	}

	@Transactional
	public Result createOrGet(UUID orderId, BigDecimal amount) {
		log.info("Payment request: orderId={}, amount={}", orderId, amount);

		var existing = paymentRepository.findByOrderId(orderId);
		if (existing.isPresent()) {
			var p = existing.get();
			log.debug("Idempotent hit: orderId={} already has status={}", orderId, p.getStatus());
			return switch (p.getStatus()) {
				case SUCCEEDED -> Result.succeeded("Already paid");
				case FAILED -> Result.failed("Already failed");
			};
		}

		var status = decide(amount);
		var payment = new PaymentEntity(orderId, amount, status);
		paymentRepository.save(payment);

		if (status == PaymentStatus.SUCCEEDED) {
			sqsEventPublisher.publish(
					paymentsQueueUrl,
					new PaymentSucceededEvent(UUID.randomUUID(), Instant.now(), orderId, amount)
			);
			log.info("Payment succeeded: orderId={}, amount={}", orderId, amount);
			return Result.succeeded("Payment succeeded");
		}

		var reason = "Mock decline (amount too high)";
		sqsEventPublisher.publish(
				paymentsQueueUrl,
				new PaymentFailedEvent(UUID.randomUUID(), Instant.now(), orderId, amount, reason)
		);
		log.warn("Payment declined: orderId={}, amount={}, reason={}", orderId, amount, reason);
		return Result.failed(reason);
	}

	@Transactional
	public RefundResult refundOrGet(UUID orderId, BigDecimal amount) {
		log.info("Refund request: orderId={}, amount={}", orderId, amount);

		var existing = paymentRepository.findByOrderId(orderId);
		if (existing.isEmpty()) {
			log.debug("No payment found for orderId={}, refund is idempotent", orderId);
			return RefundResult.refunded("No payment to refund (idempotent)");
		}

		var payment = existing.get();
		// Only refund if payment was actually successful
		if (payment.getStatus() == PaymentStatus.SUCCEEDED) {
			log.info("Refunding payment: orderId={}, amount={}", orderId, amount);
			// In a real system, we'd integrate with the payment processor here
			// For this mock, we just log it and mark as refunded conceptually
			return RefundResult.refunded("Payment refunded");
		}

		log.debug("Payment in status {} cannot be refunded: orderId={}", payment.getStatus(), orderId);
		return RefundResult.refunded("Payment already in status " + payment.getStatus() + " (idempotent)");
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

	public record RefundResult(boolean refunded, String message) {
		public static RefundResult refunded(String msg) { return new RefundResult(true, msg); }
		public static RefundResult failed(String msg) { return new RefundResult(false, msg); }
	}
}

