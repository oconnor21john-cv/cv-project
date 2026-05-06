# Java Order Microservices - Architecture & Design

This document explains the architecture and key design decisions in the order microservices system.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Web UI (React)                              │
│                      Vite / TypeScript                              │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ HTTPS
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │  Order  │      │Inventory│      │ Payment │
   │ Service │      │ Service │      │ Service │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Orders  │      │Inventory│      │Payments │
   │   DB    │      │   DB    │      │   DB    │
   └────┬────┘      └────┬────┘      └────┬────┘
        │                │                │
        └─────────────────┼─────────────────┘
                          │
                    ┌─────▼─────┐
                    │    SQS    │
                    │  3 Queues │
                    └───────────┘
```

### Services

**Order Service** (Port 8081)
- Orchestrates the confirm-order saga
- Manages order lifecycle (PLACED → CONFIRMED → CANCELLED)
- Routes requests to inventory and payment services
- Publishes domain events to SQS via outbox pattern

**Inventory Service** (Port 8082)
- Reserves and releases stock (pessimistic locking)
- Provides idempotent operations (keyed by orderId)
- Handles partial failures gracefully
- Tracks on-hand and reserved quantities

**Payment Service** (Port 8083)
- Mock payment authorization (succeeds if amount ≤ $1000)
- Refund endpoint for order cancellations
- Idempotent by orderId

### Databases

Each service has its own PostgreSQL database for true data isolation:
- `orders` – Order entities, items, and status history
- `inventory` – Stock ledger with reservations
- `payments` – Payment records (creates, refunds)

Benefits:
- Services are not blocked by other databases' locks
- Allows independent scaling and schema evolution
- Clearer service boundaries

## Order Confirmation Saga

When a user calls `POST /orders/{id}/confirm`, the system executes a distributed saga:

```
Client
  │
  ├─→ Load Order (outside txn) ─────────────────────────┐
  │                                                     │
  │   HTTP: Reserve Stock                              │
  │   ├─→ [Inventory Service]                          │
  │   │   └─→ Lock & decrement on-hand                 │
  │   │   ← RESERVED ✓                                 │
  │   │                                                 │
  │   HTTP: Create Payment                             │
  │   ├─→ [Payment Service]                            │
  │   │   ├─→ Check amount ≤ $1000                     │
  │   │   └─→ Record payment                           │
  │   │   ← SUCCEEDED ✓                                │
  │   │                                                 │
  │   ← Status update in short transaction             │
  │   └─→ [Write CONFIRMED to DB]                      │
  │   └─→ [Write OrderConfirmedEvent to outbox]        │
  │                                                     │
  └─→ OrderOutboxPoller (async)                        │
      └─→ Drain outbox → SQS queue                     │
```

### Key Design Choices

#### 1. HTTP Calls Outside Transaction

**Why:** Holding a database connection while waiting for HTTP is expensive.

```java
// ✗ BAD: Holds DB connection during HTTP calls
@Transactional
public void confirm(UUID orderId) {
    inventoryClient.reserve(...);  // 100ms+, connection held
    paymentClient.pay(...);         // 100ms+, connection held
}

// ✓ GOOD: Only hold connection when writing to DB
public void confirm(UUID orderId) {
    var reserveResp = inventoryClient.reserve(...);  // No connection
    var payResp = paymentClient.pay(...);             // No connection
    
    transactionalWriter.confirmOrder(order);  // Short txn: just write
}
```

At scale with 50 concurrent users, bad approach exhausts a 10-connection pool (100ms × 10 = 1 second latency spike).

#### 2. Pessimistic Locking on Inventory

**Why:** Optimistic locking (retries on conflict) causes excessive coordination in a high-contention shared resource.

```sql
-- Pessimistic: Reserve atomically, fail fast if not enough stock
SELECT on_hand FROM stock WHERE sku = ? FOR UPDATE;
-- Decrement

-- Optimistic: Retry if version changed (many retries under load)
UPDATE stock SET on_hand = on_hand - ?, version = version + 1 
  WHERE sku = ? AND version = ?;
```

For shared inventory (e.g., 5 units of "SKU-APPLE"), pessimistic avoids the thundering herd.

#### 3. Idempotent Reservations (by orderId)

**Why:** Network failures can cause duplicate requests.

```
Request: Reserve(orderId=123, qty=2)
Server persists: INSERT INTO reservations (order_id, qty) ...
Response is lost in network.

Client retries: Reserve(orderId=123, qty=2)
Server checks: SELECT * FROM reservations WHERE order_id = 123
→ Already reserved. Return success (idempotent).
```

Without idempotency, retry would double-deduct stock.

#### 4. Outbox Pattern for Event Publishing

**Why:** Ensure DB and SQS are never out of sync.

```
Naive:
  1. UPDATE orders SET status = 'CONFIRMED'  ← succeeds
  2. SQS publish                             ← fails, network down
  Result: DB says CONFIRMED, no event. Subscribers miss the update.

Outbox:
  1. UPDATE orders SET status = 'CONFIRMED'
  2. INSERT INTO order_outbox (event)        ← same txn
  3. COMMIT                                  ← atomic
  Later: Poller reads outbox, publishes to SQS, marks sent.
  Result: Always in sync. If SQS is down, poller retries.
```

#### 5. Circuit Breaker (50% failure rate, 30s reset)

**Why:** Fast-fail degradation. Don't wait for a hung service.

```
Healthy     Normal calls      (< 50% failures)
  │                 
  └─→ Open   (fail fast, retry after 30s) ← 50%+ failures detected
        │
        └─→ Half-Open (1 test call) ← 30s elapsed
              │
              ├─→ Success → Healthy
              └─→ Failure → Open
```

If payment-service hangs, order confirmation fails quickly (ms) instead of timing out (seconds).

#### 6. JWT with HS256 and Issuer Validation

**Why:** Token scope and origin validation.

```java
// Decoder enforces issuer claim
JwtValidators.createDefaultWithIssuer("portfolio")
  // Reject tokens from other systems (e.g., "accounts-service")
  // Reject tokens without iss claim (missing claim = reject)
```

## File Structure

```
order-service/
├── src/main/java/com/portfolio/order/
│   ├── api/              # REST controllers, exceptions, responses
│   ├── clients/          # HTTP clients to other services
│   ├── domain/           # OrderStatus enum
│   ├── events/           # Domain events (OrderPlacedEvent, ...)
│   ├── messaging/        # SQS & outbox publishing
│   ├── persistence/      # JPA entities, repositories
│   └── service/          # Business logic, OrderService, transactional writer
├── src/main/resources/
│   ├── application.properties
│   ├── db/migration/     # Flyway SQL migrations (V1__, V2__, ...)
├── src/test/
│   └── java/...          # Integration tests with Testcontainers, WireMock
└── build.gradle.kts

inventory-service/, payment-service/  # Similar structure
```

## Technology Stack

- **Spring Boot 3** – REST APIs, dependency injection
- **Spring Security** – OAuth2 resource server, JWT
- **Spring Data JPA** – ORM
- **Postgres 15** – ACID database
- **Flyway** – Database versioning
- **AWS SQS** – Event queue
- **Resilience4j** – Circuit breaker
- **Testcontainers** – Integration tests (spins up Postgres)
- **WireMock** – Mock external services

## Security

1. **Authentication:** BCrypt-hashed passwords in `users` table, HS256 JWT tokens
2. **Authorization:** Spring Security roles (CUSTOMER, ADMIN)
3. **JWT Hardening:**
   - Issuer claim validation (`iss: "portfolio"`)
   - 32-character minimum secret (256 bits for HS256)
   - Dev secret rejected in non-local profiles at startup
4. **Data Isolation:** Each user can only access their own orders

## Testing

```bash
cd order-service
./gradlew test
```

Integration tests:
- Use Testcontainers to spawn Postgres
- Use WireMock to stub inventory/payment services
- Verify saga behavior: happy path, failure handling, retries

## Deployment

For local development:
```bash
docker compose up --build
# Order service: http://localhost:8081
# Inventory: http://localhost:8082
# Payment: http://localhost:8083
```

For production:
- Deploy each service independently on a container platform (Railway, Fly.io, etc.)
- Use managed RDS PostgreSQL for each database
- Use AWS SQS (no mock needed)
- Set `JWT_SECRET` environment variable (32+ chars)
- Use Spring profiles (`prod`, `staging`) to control feature flags

## Known Limitations

1. **Payment refund is mock:** Real implementation would integrate with a payment processor (Stripe, etc.)
2. **Single warehouse:** No multi-region inventory rebalancing
3. **SQS only:** Could extend to SNS for event broadcast
4. **No distributed tracing:** Add Jaeger/OpenTelemetry for observability at scale
