package com.portfolio.order;

import static com.github.tomakehurst.wiremock.client.WireMock.*;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;
import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.TestPropertySource;
import org.testcontainers.containers.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

import com.github.tomakehurst.wiremock.WireMockServer;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
@TestPropertySource(properties = {
		"spring.flyway.enabled=true",
		"spring.jpa.hibernate.ddl-auto=validate"
})
class OrderFlowIntegrationTest {

	@Container
	static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
			.withDatabaseName("orders")
			.withUsername("orders")
			.withPassword("orders");

	static WireMockServer inventoryMock = new WireMockServer(wireMockConfig().dynamicPort());
	static WireMockServer paymentMock = new WireMockServer(wireMockConfig().dynamicPort());

	static {
		inventoryMock.start();
		paymentMock.start();
	}

	@DynamicPropertySource
	static void configure(DynamicPropertyRegistry registry) {
		registry.add("spring.datasource.url", postgres::getJdbcUrl);
		registry.add("spring.datasource.username", postgres::getUsername);
		registry.add("spring.datasource.password", postgres::getPassword);
		registry.add("app.inventory.base-url", inventoryMock::baseUrl);
		registry.add("app.payment.base-url", paymentMock::baseUrl);
		registry.add("app.sqs.enabled", () -> "false");
	}

	@Autowired
	TestRestTemplate rest;

	@AfterAll
	static void stopMocks() {
		inventoryMock.stop();
		paymentMock.stop();
	}

	@BeforeEach
	void resetMocks() {
		inventoryMock.resetAll();
		paymentMock.resetAll();
	}

	// ── helpers ──────────────────────────────────────────────────────────────────

	private String obtainToken() {
		var body = Map.of("username", "customer", "password", "password");
		var resp = rest.postForEntity("/auth/token", body, Map.class);
		assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.OK);
		return (String) resp.getBody().get("accessToken");
	}

	private HttpHeaders bearerHeaders(String token) {
		var h = new HttpHeaders();
		h.setBearerAuth(token);
		h.setContentType(MediaType.APPLICATION_JSON);
		return h;
	}

	@SuppressWarnings("unchecked")
	private Map<String, Object> createOrder(HttpHeaders headers) {
		stubInventoryPrices();
		var json = """
				{"items":[{"sku":"SKU-APPLE","quantity":2}]}""";
		var resp = rest.exchange("/orders", HttpMethod.POST,
				new HttpEntity<>(json, headers), Map.class);
		assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.OK);
		return resp.getBody();
	}

	// ── tests ────────────────────────────────────────────────────────────────────

	@Test
	void happyPath_createConfirmCancelOrder() {
		stubInventoryReserveOk();
		stubPaymentOk();
		stubInventoryReleaseOk();

		var token = obtainToken();
		var headers = bearerHeaders(token);

		// create
		var order = createOrder(headers);
		assertThat(order.get("status")).isEqualTo("PLACED");
		var orderId = (String) order.get("id");

		// confirm (reserve + pay)
		var confirm = rest.exchange("/orders/" + orderId + "/confirm",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(confirm.getStatusCode())
				.as("confirm response body: %s", confirm.getBody())
				.isEqualTo(HttpStatus.OK);
		assertThat(confirm.getBody().get("status")).isEqualTo("CONFIRMED");

		// cancel (should release inventory)
		var cancel = rest.exchange("/orders/" + orderId + "/cancel",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(cancel.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(cancel.getBody().get("status")).isEqualTo("CANCELLED");

		inventoryMock.verify(deleteRequestedFor(urlPathMatching("/reservations/.*")));

		// verify final state
		var get = rest.exchange("/orders/" + orderId, HttpMethod.GET,
				new HttpEntity<>(headers), Map.class);
		assertThat(get.getBody().get("status")).isEqualTo("CANCELLED");
	}

	@Test
	void cancelPlacedOrder_noCompensationNeeded() {
		var token = obtainToken();
		var headers = bearerHeaders(token);

		var order = createOrder(headers);
		var orderId = (String) order.get("id");

		var cancel = rest.exchange("/orders/" + orderId + "/cancel",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(cancel.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(cancel.getBody().get("status")).isEqualTo("CANCELLED");

		inventoryMock.verify(0, deleteRequestedFor(urlPathMatching("/reservations/.*")));
	}

	@Test
	void cancelAlreadyCancelledOrder_returns409() {
		var token = obtainToken();
		var headers = bearerHeaders(token);

		var order = createOrder(headers);
		var orderId = (String) order.get("id");

		rest.exchange("/orders/" + orderId + "/cancel",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);

		var second = rest.exchange("/orders/" + orderId + "/cancel",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(second.getStatusCode()).isEqualTo(HttpStatus.CONFLICT);
	}

	@Test
	void confirmWithPaymentFailure_releasesStockAndSetsPaymentFailed() {
		stubInventoryReserveOk();
		stubInventoryReleaseOk();
		paymentMock.stubFor(post(urlEqualTo("/payments"))
				.willReturn(okJson("""
						{"status":"FAILED","message":"Insufficient funds"}""")));

		var token = obtainToken();
		var headers = bearerHeaders(token);

		var order = createOrder(headers);
		var orderId = (String) order.get("id");

		var confirm = rest.exchange("/orders/" + orderId + "/confirm",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(confirm.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(confirm.getBody().get("status")).isEqualTo("PAYMENT_FAILED");

		inventoryMock.verify(deleteRequestedFor(urlPathMatching("/reservations/.*")));
	}

	@Test
	void confirmWithInventoryFailure_setsStockFailed() {
		inventoryMock.stubFor(post(urlEqualTo("/reservations"))
				.willReturn(aResponse()
						.withStatus(400)
						.withHeader("Content-Type", "application/json")
						.withBody("""
								{"status":"FAILED","message":"Out of stock"}""")));

		var token = obtainToken();
		var headers = bearerHeaders(token);

		var order = createOrder(headers);
		var orderId = (String) order.get("id");

		var confirm = rest.exchange("/orders/" + orderId + "/confirm",
				HttpMethod.POST, new HttpEntity<>(null, headers), Map.class);
		assertThat(confirm.getStatusCode()).isEqualTo(HttpStatus.OK);
		assertThat(confirm.getBody().get("status")).isEqualTo("STOCK_FAILED");

		paymentMock.verify(0, postRequestedFor(urlEqualTo("/payments")));
	}

	@Test
	void unauthenticatedRequest_returns401() {
		var resp = rest.exchange("/orders", HttpMethod.POST,
				new HttpEntity<>("""
						{"items":[{"sku":"X","quantity":1,"unitPrice":1}]}""",
						jsonHeaders()),
				Map.class);
		assertThat(resp.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
	}

	// ── WireMock stubs ───────────────────────────────────────────────────────────

	private void stubInventoryReserveOk() {
		inventoryMock.stubFor(post(urlEqualTo("/reservations"))
				.willReturn(okJson("""
						{"status":"RESERVED","message":"ok"}""")));
	}

	private void stubPaymentOk() {
		paymentMock.stubFor(post(urlEqualTo("/payments"))
				.willReturn(okJson("""
						{"status":"SUCCEEDED","message":"ok"}""")));
	}

	private void stubInventoryPrices() {
		inventoryMock.stubFor(get(urlPathEqualTo("/products/prices"))
				.willReturn(okJson("""
						{"SKU-APPLE":0.50}""")));
	}

	private void stubInventoryReleaseOk() {
		inventoryMock.stubFor(delete(urlPathMatching("/reservations/.*"))
				.willReturn(okJson("""
						{"status":"RELEASED","message":"ok"}""")));
	}

	private HttpHeaders jsonHeaders() {
		var h = new HttpHeaders();
		h.setContentType(MediaType.APPLICATION_JSON);
		return h;
	}
}
