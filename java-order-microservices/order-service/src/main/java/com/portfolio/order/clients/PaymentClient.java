package com.portfolio.order.clients;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;

@Component
public class PaymentClient {
	private final RestClient paymentRestClient;

	public PaymentClient(@Qualifier("paymentRestClient") RestClient paymentRestClient) {
		this.paymentRestClient = paymentRestClient;
	}

	@CircuitBreaker(name = "payment")
	public PaymentCreateResponse createPayment(PaymentCreateRequest request) {
		return paymentRestClient.post()
				.uri("/payments")
				.contentType(MediaType.APPLICATION_JSON)
				.body(request)
				.retrieve()
				.body(PaymentCreateResponse.class);
	}

	@CircuitBreaker(name = "payment")
	public PaymentRefundResponse refundPayment(PaymentRefundRequest request) {
		return paymentRestClient.post()
				.uri("/payments/refund")
				.contentType(MediaType.APPLICATION_JSON)
				.body(request)
				.retrieve()
				.body(PaymentRefundResponse.class);
	}
}
