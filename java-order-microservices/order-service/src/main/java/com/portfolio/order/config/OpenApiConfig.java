package com.portfolio.order.config;

import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.enums.SecuritySchemeType;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.security.SecurityScheme;
import org.springframework.context.annotation.Configuration;

@Configuration
@OpenAPIDefinition(
		info = @Info(
				title = "Order Service API",
				version = "1.0",
				description = "REST API for creating, confirming, and cancelling orders"
		),
		security = @SecurityRequirement(name = "bearer-jwt")
)
@SecurityScheme(
		name = "bearer-jwt",
		type = SecuritySchemeType.HTTP,
		scheme = "bearer",
		bearerFormat = "JWT",
		description = "Use POST /auth/token to obtain a JWT, then paste it here"
)
public class OpenApiConfig {
}
