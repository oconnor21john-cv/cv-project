package com.portfolio.order.clients;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration
public class ClientsConfig {
	@Bean(name = "inventoryRestClient")
	RestClient inventoryRestClient(@Value("${app.inventory.base-url}") String baseUrl) {
		return RestClient.builder().baseUrl(baseUrl).build();
	}

	@Bean(name = "paymentRestClient")
	RestClient paymentRestClient(@Value("${app.payment.base-url}") String baseUrl) {
		return RestClient.builder().baseUrl(baseUrl).build();
	}
}

