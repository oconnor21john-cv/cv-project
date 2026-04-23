package com.portfolio.order.clients;

import java.net.http.HttpClient;

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
				.build();
		return new JdkClientHttpRequestFactory(httpClient);
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

