package com.portfolio.order.security;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/auth")
public class AuthController {
	private final JwtEncoder jwtEncoder;
	private final String issuer;

	public AuthController(JwtEncoder jwtEncoder, @Value("${app.security.jwt.issuer}") String issuer) {
		this.jwtEncoder = jwtEncoder;
		this.issuer = issuer;
	}

	@PostMapping("/token")
	public TokenResponse token(@Valid @RequestBody TokenRequest request) {
		var roles = authenticate(request.username(), request.password());
		if (roles == null) {
			throw new InvalidCredentialsException();
		}

		var now = Instant.now();
		var claims = JwtClaimsSet.builder()
				.issuer(issuer)
				.issuedAt(now)
				.expiresAt(now.plus(60, ChronoUnit.MINUTES))
				.subject(request.username())
				.claim("roles", roles)
				.build();

		var headers = JwsHeader.with(MacAlgorithm.HS256).build();
		var token = jwtEncoder.encode(JwtEncoderParameters.from(headers, claims)).getTokenValue();
		return new TokenResponse(token, "Bearer");
	}

	private List<String> authenticate(String username, String password) {
		if ("customer".equals(username) && "password".equals(password)) {
			return List.of("CUSTOMER");
		}
		if ("admin".equals(username) && "password".equals(password)) {
			return List.of("ADMIN");
		}
		return null;
	}

	@ResponseStatus(HttpStatus.UNAUTHORIZED)
	private static class InvalidCredentialsException extends RuntimeException {}
}

