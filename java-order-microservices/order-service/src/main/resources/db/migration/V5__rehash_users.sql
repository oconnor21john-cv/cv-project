-- V5__rehash_users.sql
-- Re-hash seeded users with a verified BCrypt hash for "password".
--
-- The hash in V3 was malformed; we rehash here rather than mutate V3 to keep
-- migration history immutable. This is an important Flyway invariant: migrations
-- are append-only. Once a migration has run on any database, it must never be
-- changed — doing so breaks the checksum contract and forces manual repair.
--
-- This migration is idempotent: it works whether the DB is fresh (V3 just seeded
-- the bad hash) or already-patched (you ran the manual UPDATE earlier today).
--
-- NOTE: The plaintext "password" is dev/test only. A real production system would
-- never seed user credentials via migrations at all.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

UPDATE users
SET password_hash = crypt('password', gen_salt('bf', 10))
WHERE username IN ('customer', 'admin');
