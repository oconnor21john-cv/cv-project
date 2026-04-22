package com.portfolio.payment.api;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.portfolio.payment.service.PaymentService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/payments")
public class PaymentController {
	private final PaymentService paymentService;

	public PaymentController(PaymentService paymentService) {
		this.paymentService = paymentService;
	}

	@PostMapping
	public ResponseEntity<CreatePaymentResponse> create(@Valid @RequestBody CreatePaymentRequest request) {
		var result = paymentService.createOrGet(request.orderId(), request.amount());
		if (result.succeeded()) {
			return ResponseEntity.ok(new CreatePaymentResponse("SUCCEEDED", result.message()));
		}
		return ResponseEntity.badRequest().body(new CreatePaymentResponse("FAILED", result.message()));
	}
}

