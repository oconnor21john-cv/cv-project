# Java Order Microservices (Spring Boot + AWS SQS)

Portfolio-sized microservices demo:

- `order-service` (JWT-secured): create/confirm/cancel orders (orchestrates reserve stock + payment)
- `inventory-service`: reserves/releases stock (idempotent by `orderId`)
- `payment-service`: mock payment authorize/decline (idempotent by `orderId`)
- SQS event publishing: one queue per service (`order-service`, `inventory-service`, `payment-service`)
- Separate Postgres DB per service + Flyway migrations
- Swagger UI on every service
- Testcontainers + WireMock integration tests

## Prereqs

- Docker Desktop

## Run

From this folder:

```powershell
docker compose up --build
```

Services:

| Service | URL | Swagger UI |
|---------|-----|------------|
| Order Service | `http://localhost:8081` | [swagger-ui](http://localhost:8081/swagger-ui.html) |
| Inventory Service | `http://localhost:8082` | [swagger-ui](http://localhost:8082/swagger-ui.html) |
| Payment Service | `http://localhost:8083` | [swagger-ui](http://localhost:8083/swagger-ui.html) |
| Web UI | `http://localhost:5173` | — |

## Get a JWT

```powershell
$token = (Invoke-RestMethod -Method Post -Uri http://localhost:8081/auth/token `
  -ContentType 'application/json' `
  -Body (@{ username = 'customer'; password = 'password' } | ConvertTo-Json)).accessToken

$token
```

Use it as `Bearer <token>`.

## Create + confirm an order

```powershell
# Create order
$order = Invoke-RestMethod -Method Post -Uri http://localhost:8081/orders `
  -Headers @{ Authorization = "Bearer $token" } `
  -ContentType 'application/json' `
  -Body (@{ items = @(@{ sku='SKU-APPLE'; quantity=2; unitPrice=0.50 }) } | ConvertTo-Json)

# Confirm (reserve stock -> pay)
$confirmed = Invoke-RestMethod -Method Post -Uri ("http://localhost:8081/orders/{0}/confirm" -f $order.id) `
  -Headers @{ Authorization = "Bearer $token" }

$confirmed
```

## Cancel an order (compensation)

```powershell
$cancelled = Invoke-RestMethod -Method Post -Uri ("http://localhost:8081/orders/{0}/cancel" -f $order.id) `
  -Headers @{ Authorization = "Bearer $token" }

$cancelled
```

If the order was CONFIRMED, the cancel will release the reserved inventory automatically.

## Run integration tests

Requires Docker running (Testcontainers spins up Postgres):

```powershell
cd order-service
.\gradlew test
```

## Deploying the web UI to Netlify

Netlify hosts the **React frontend only**. The three Spring Boot services (plus Postgres) must be deployed separately on a server platform — [Railway](https://railway.app), [Render](https://render.com), or [Fly.io](https://fly.io) all work well with Docker Compose.

### Steps

1. Push this repository to GitHub / GitLab / Bitbucket.
2. In the Netlify dashboard click **Add new site → Import an existing project** and connect your repo.
3. Netlify auto-detects the `netlify.toml` at the root — no manual build settings needed:
   - **Base directory:** `web-ui`
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`
4. Go to **Site → Environment variables** and add:

   | Key | Value |
   |-----|-------|
   | `VITE_API_BASE_URL` | `https://your-deployed-order-service.example.com` |

   This URL is baked into the frontend at build time by Vite.
5. Click **Deploy site**. Netlify installs dependencies and runs `npm run build` inside `web-ui/`.

### CORS

Once the frontend is live on a `*.netlify.app` domain you must allow that origin in the `order-service`. Add the Netlify URL to the CORS configuration in `order-service` (or set it via the `CORS_ALLOWED_ORIGINS` environment variable if you wire one up).

### Local development still works

```powershell
docker compose up --build   # starts all backend services
cd web-ui
npm install
npm run dev                 # uses .env (VITE_API_BASE_URL=http://localhost:8081)
```

## Notes

- The inventory DB is seeded with a few SKUs (see `inventory-service` Flyway migrations).
- Payment is a mock: amounts > 1000.00 are declined.
- The build is configured for Java 25 (to match your installed JDK). You can change all `build.gradle` toolchains + Dockerfiles to Java 17 if you want.

## AWS deployment starter

Infrastructure-as-code and CI/CD bootstrap files are included:

- Terraform stack: `infra/terraform`
- GitHub Actions deploy pipeline: `.github/workflows/deploy-ecs.yml`

See `infra/terraform/README.md` for step-by-step setup and required variables/secrets.

