package com.portfolio.order.persistence;

import java.time.Instant;
import java.util.Arrays;
import java.util.Collection;
import java.util.UUID;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * User entity with BCrypt password storage for Spring Security integration.
 */
@Entity
@Table(name = "users")
public class UserEntity implements UserDetails {
	@Id
	private UUID id;

	@Column(nullable = false, unique = true, length = 255)
	private String username;

	@Column(nullable = false, name = "password_hash", length = 255)
	private String passwordHash;

	@Column(nullable = false, length = 255)
	private String roles;

	@Column(nullable = false)
	private boolean enabled;

	@Column(nullable = false, name = "created_at")
	private Instant createdAt;

	@Column(nullable = false, name = "updated_at")
	private Instant updatedAt;

	protected UserEntity() {
	}

	public UserEntity(String username, String passwordHash, String roles) {
		this.id = UUID.randomUUID();
		this.username = username;
		this.passwordHash = passwordHash;
		this.roles = roles;
		this.enabled = true;
		this.createdAt = Instant.now();
		this.updatedAt = Instant.now();
	}

	// UserDetails interface implementation
	@Override
	public Collection<? extends GrantedAuthority> getAuthorities() {
		return Arrays.stream(roles.split(","))
				.map(String::trim)
				.map(role -> !role.startsWith("ROLE_") ? "ROLE_" + role : role)
				.map(SimpleGrantedAuthority::new)
				.toList();
	}

	@Override
	public String getPassword() {
		return passwordHash;
	}

	@Override
	public String getUsername() {
		return username;
	}

	@Override
	public boolean isAccountNonExpired() {
		return enabled;
	}

	@Override
	public boolean isAccountNonLocked() {
		return enabled;
	}

	@Override
	public boolean isCredentialsNonExpired() {
		return enabled;
	}

	@Override
	public boolean isEnabled() {
		return enabled;
	}

	// Getters for entity fields
	public UUID getId() {
		return id;
	}

	public String getRoles() {
		return roles;
	}

	public Instant getCreatedAt() {
		return createdAt;
	}

	public Instant getUpdatedAt() {
		return updatedAt;
	}
}
