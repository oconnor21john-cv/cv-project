-- Create users table for BCrypt authentication
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    roles VARCHAR(255) NOT NULL DEFAULT 'CUSTOMER',
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);

-- Insert default users (passwords are BCrypted: "password" -> "$2a$10$YIjlrHMkV.xekmh7ZEkB5.WqfBIECRXFxDNzZ1F6dC3P5LqU4Z7Hy")
-- You can use Spring Security's BCryptPasswordEncoder with strength 10 to generate new hashes
INSERT INTO users (id, username, password_hash, roles, enabled) VALUES
    ('550e8400-e29b-41d4-a716-446655440001', 'customer', '$2a$10$YIjlrHMkV.xekmh7ZEkB5.WqfBIECRXFxDNzZ1F6dC3P5LqU4Z7Hy', 'CUSTOMER', true),
    ('550e8400-e29b-41d4-a716-446655440002', 'admin', '$2a$10$YIjlrHMkV.xekmh7ZEkB5.WqfBIECRXFxDNzZ1F6dC3P5LqU4Z7Hy', 'ADMIN', true);
