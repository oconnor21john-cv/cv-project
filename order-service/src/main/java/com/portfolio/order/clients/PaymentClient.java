package com.portfolio.order.clients;

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

	public PaymentCreateResponse createPayment(PaymentCreateRequest request) {
		return paymentRestClient.post()
				.uri("/payments")
				.contentType(MediaType.APPLICATION_JSON)
				.body(request)
				.retrieve()
				.body(PaymentCreateResponse.class);
	}
}

