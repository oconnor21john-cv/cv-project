package com.portfolio.order.security;

import java.nio.charset.StandardCharsets;
import java.util.Collection;
import java.util.stream.Collectors;

import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.core.annotation.Order;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtValidators;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.util.matcher.OrRequestMatcher;
import org.springframework.security.web.util.matcher.PathPatternRequestMatcher;

import com.nimbusds.jose.jwk.source.ImmutableSecret;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
	@Bean
	@Order(1)
	SecurityFilterChain publicEndpoints(HttpSecurity http) throws Exception {
		http.securityMatcher(new OrRequestMatcher(
				PathPatternRequestMatcher.withDefaults().matcher("/auth/**"),
				PathPatternRequestMatcher.withDefaults().matcher("/actuator/**"),
				PathPatternRequestMatcher.withDefaults().matcher("/swagger-ui/**"),
				PathPatternRequestMatcher.withDefaults().matcher("/swagger-ui.html"),
				PathPatternRequestMatcher.withDefaults().matcher("/v3/api-docs/**")
		));
		http.cors(cors -> {});
		http.csrf(csrf -> csrf.disable());
		http.authorizeHttpRequests(auth -> auth.anyRequest().permitAll());
		return http.build();
	}

	@Bean
	@Order(2)
	SecurityFilterChain apiEndpoints(HttpSecurity http, JwtAuthenticationConverter jwtAuthConverter) throws Exception {
		http.securityMatcher(new OrRequestMatcher(
				PathPatternRequestMatcher.withDefaults().matcher("/orders/**"),
				PathPatternRequestMatcher.withDefaults().matcher("/catalog/**")
		));
		http.cors(cors -> {});
		http.csrf(csrf -> csrf.disable());
		http.authorizeHttpRequests(auth -> auth
				.requestMatchers(HttpMethod.OPTIONS, "/**").permitAll()
				.requestMatchers(HttpMethod.GET, "/orders/**").hasAnyRole("CUSTOMER", "ADMIN")
				.requestMatchers(HttpMethod.POST, "/orders/**").hasAnyRole("CUSTOMER", "ADMIN")
				.requestMatchers(HttpMethod.DELETE, "/orders/**").hasAnyRole("CUSTOMER", "ADMIN")
				.requestMatchers(HttpMethod.GET, "/catalog/**").hasAnyRole("CUSTOMER", "ADMIN")
				.anyRequest().authenticated()
		);
		http.oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter)));
		return http.build();
	}

	@Bean
	JwtAuthenticationConverter jwtAuthenticationConverter() {
		var converter = new JwtAuthenticationConverter();
		converter.setJwtGrantedAuthoritiesConverter(this::rolesToAuthorities);
		return converter;
	}

	private Collection<GrantedAuthority> rolesToAuthorities(Jwt jwt) {
		var roles = jwt.getClaimAsStringList("roles");
		if (roles == null) {
			return java.util.List.of();
		}
		return roles.stream()
				.map(r -> "ROLE_" + r)
				.map(SimpleGrantedAuthority::new)
				.collect(Collectors.toList());
	}

	@Bean
	PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder(10);
	}

	@Bean
	AuthenticationManager authenticationManager(HttpSecurity http, UserDetailsService userDetailsService,
			PasswordEncoder passwordEncoder) throws Exception {
		var authProvider = new DaoAuthenticationProvider();
		authProvider.setUserDetailsService(userDetailsService);
		authProvider.setPasswordEncoder(passwordEncoder);
		var builder = http.getSharedObject(AuthenticationManagerBuilder.class);
		builder.authenticationProvider(authProvider);
		return builder.build();
	}

	@Bean
	SecretKey jwtSecretKey(@Value("${app.security.jwt.secret}") String secret) {
		return new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
	}

	@Bean
	JwtDecoder jwtDecoder(SecretKey jwtSecretKey, @Value("${app.security.jwt.issuer}") String issuer) {
		var decoder = NimbusJwtDecoder.withSecretKey(jwtSecretKey)
				.macAlgorithm(MacAlgorithm.HS256)
				.build();
		// Enforce issuer validation for additional security
		decoder.setJwtValidator(JwtValidators.createDefaultWithIssuer(issuer));
		return decoder;
	}

	@Bean
	JwtEncoder jwtEncoder(SecretKey jwtSecretKey) {
		return new NimbusJwtEncoder(new ImmutableSecret<>(jwtSecretKey));
	}
}

