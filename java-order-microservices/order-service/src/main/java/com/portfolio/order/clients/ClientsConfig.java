package com.portfolio.order.clients;

import java.net.http.HttpClient;
import java.time.Duration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.JdkClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

@Configuration
public class ClientsConfig {

	private JdkClientHttpRequestFactory http11RequestFactory() {
		var httpClient = HttpClient.newBuilder()
				.version(HttpClient.Version.HTTP_1_1)
				.connectTimeout(Duration.ofSeconds(2))
				.build();

		var requestFactory = new JdkClientHttpRequestFactory(httpClient);
		// Set read timeout for individual requests
		requestFactory.setReadTimeout(Duration.ofSeconds(10));
		return requestFactory;
	}

	@Bean(name = "inventoryRestClient")
	RestClient inventoryRestClient(@Value("${app.inventory.base-url}") String baseUrl) {
		return RestClient.builder()
				.baseUrl(baseUrl)
				.requestFactory(http11RequestFactory())
				.build();
	}

	@Bean(name = "paymentRestClient")
	RestClient paymentRestClient(@Value("${app.payment.base-url}") String baseUrl) {
		return RestClient.builder()
				.baseUrl(baseUrl)
				.requestFactory(http11RequestFactory())
				.build();
	}
}

