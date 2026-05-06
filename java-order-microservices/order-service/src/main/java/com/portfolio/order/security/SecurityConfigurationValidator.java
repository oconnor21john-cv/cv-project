package com.portfolio.order.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;

import jakarta.annotation.PostConstruct;

/**
 * Validates security configuration at startup.
 * Fails fast if the dev JWT secret is used in non-local profiles.
 */
@Configuration
@EnableConfigurationProperties
public class SecurityConfigurationValidator {
	private final String jwtSecret;
	private final Environment environment;

	public SecurityConfigurationValidator(
			@Value("${app.security.jwt.secret:}") String jwtSecret,
			Environment environment
	) {
		this.jwtSecret = jwtSecret;
		this.environment = environment;
	}

	@PostConstruct
	public void validateJwtConfiguration() {
		// Check if JWT_SECRET is not set or is empty
		if (jwtSecret == null || jwtSecret.isBlank()) {
			String profile = getActiveProfile();
			if ("local".equals(profile) || "test".equals(profile)) {
				throw new IllegalStateException(
						"SECURITY ERROR: JWT_SECRET is not set. "
						+ "For local development, add application-local.properties with dev secret."
				);
			} else {
				throw new IllegalStateException(
						"SECURITY ERROR: JWT_SECRET environment variable is required for profile '" + profile + "'. "
						+ "Set a secure secret (minimum 32 characters, 256 bits for HS256)."
				);
			}
		}

		// Check if using dev secret in non-local profiles
		if ("dev-secret-change-me-please-use-at-least-32-bytes".equals(jwtSecret)) {
			String profile = getActiveProfile();
			if (!"local".equals(profile) && !"test".equals(profile)) {
				throw new IllegalStateException(
						"SECURITY ERROR: Using dev JWT secret in profile '" + profile + "'. "
						+ "Set the JWT_SECRET environment variable to a secure value (min 32 chars)."
				);
			}
		}

		// Check minimum length (32 bytes = 256 bits for HS256)
		if (jwtSecret.length() < 32) {
			throw new IllegalStateException(
					"SECURITY ERROR: JWT_SECRET is too short. Minimum 32 characters required, got " + jwtSecret.length() + ". "
					+ "HS256 requires at least 256 bits (32 bytes) of entropy."
			);
		}
	}

	private String getActiveProfile() {
		String[] profiles = environment.getActiveProfiles();
		if (profiles.length == 0) {
			profiles = environment.getDefaultProfiles();
		}
		return profiles.length > 0 ? profiles[0] : "default";
	}
}
