package com.portfolio.order.security;

public record TokenResponse(
		String accessToken,
		String tokenType
) {}

