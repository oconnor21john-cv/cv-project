package com.portfolio.order.security;

import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
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

/**
 * Authenticates users with BCrypted passwords and issues JWT tokens.
 */
@RestController
@RequestMapping("/auth")
public class AuthController {
	private final AuthenticationManager authenticationManager;
	private final JwtEncoder jwtEncoder;
	private final String issuer;

	public AuthController(
			AuthenticationManager authenticationManager,
			JwtEncoder jwtEncoder,
			@Value("${app.security.jwt.issuer}") String issuer
	) {
		this.authenticationManager = authenticationManager;
		this.jwtEncoder = jwtEncoder;
		this.issuer = issuer;
	}

	/**
	 * Authenticates the user and returns a JWT token valid for 60 minutes.
	 */
	@PostMapping("/token")
	public TokenResponse token(@Valid @RequestBody TokenRequest request) {
		try {
			var auth = authenticationManager.authenticate(
					new UsernamePasswordAuthenticationToken(request.username(), request.password())
			);

			// Extract roles from authorities
			var roles = auth.getAuthorities().stream()
					.map(a -> a.getAuthority().replaceFirst("^ROLE_", ""))
					.collect(Collectors.toList());

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
		} catch (BadCredentialsException ex) {
			throw new InvalidCredentialsException();
		}
	}

	@ResponseStatus(HttpStatus.UNAUTHORIZED)
	private static class InvalidCredentialsException extends RuntimeException {
		public InvalidCredentialsException() {
			super("Invalid credentials");
		}
	}
}

