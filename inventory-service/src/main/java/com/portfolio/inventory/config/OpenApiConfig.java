package com.portfolio.inventory.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
		info = @Info(
				title = "Inventory Service API",
				version = "1.0",
				description = "REST API for managing inventory reservations and stock"
		)
)
public class OpenApiConfig {
}
