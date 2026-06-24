# Cost-optimised AWS stack

Rewrite of the original ALB + 3xRDS + on-demand Fargate stack focused on
cutting the monthly bill from roughly $119 to roughly $20 while keeping the
"microservices on AWS" architecture intact.

## What changed

| Concern             | Before                                | After                                                              | Est. saving |
| ------------------- | ------------------------------------- | ------------------------------------------------------------------ | ----------- |
| ECS compute         | Fargate on-demand, 24/7               | Fargate Spot + EventBridge scheduled scale-to-zero                 | ~$40/mo     |
| Databases           | 3 x `db.t3.micro` Postgres (24/7)     | 1 x `db.t4g.micro` Postgres, 3 databases, stopped overnight        | ~$30/mo     |
| Public ingress      | Application Load Balancer ($16+ idle) | API Gateway HTTP API + VPC Link (per-request, near-zero idle)      | ~$14/mo     |
| Secrets             | 4 x Secrets Manager entries           | 1 x Secrets Manager (DB master) + SSM Parameter Store (JWT)        | ~$1/mo      |
| Image storage       | Unbounded ECR                         | ECR lifecycle policy keeps only 5 most recent images per repo      | ~$1/mo      |
| **Total**           | **~$119/mo**                          | **~$20/mo with scheduler enabled, ~$45/mo always-on**              | **~$80-100/mo** |

The VPC stays NAT-less. ECS tasks live in public subnets with public IPs —
the only material cost is $0.005/hr per public IPv4, bounded by the
scheduler.

## Layout

```
infra/terraform/
  main.tf             provider, common locals, the services{} catalog
  vpc.tf              VPC, IGW, public subnets, all security groups
  database.tf         single shared Postgres instance + per-service JDBC URLs
  secrets.tf          DB master secret (Secrets Manager) + JWT (SSM Parameter Store)
  ecr.tf              ECR repos, CloudWatch log groups, SQS queues, Cloud Map service discovery
  iam.tf              ECS execution / task roles, Lambda roles, EventBridge role
  lambdas.tf          build + db_bootstrap + scheduler Lambda functions
  ecs.tf              cluster (Fargate Spot), task definitions, services
  api_gateway.tf      HTTP API + VPC Link replacing the ALB
  scheduler.tf        EventBridge schedules for sleep/wake
  outputs.tf          api_endpoint, db_endpoint, scheduler_lambda_name, ...
  variables.tf
  lambda/
    db_bootstrap.py   Creates the 3 service databases on first apply (idempotent)
    scheduler.py      Sleep/wake handler invoked by EventBridge
    build.py          Cross-platform packager; runs `pip install pg8000` into ./build
```

## Prerequisites

* Terraform `>= 1.6`
* AWS CLI configured (`aws configure`)
* Python 3.9+ on PATH (Terraform invokes `python lambda/build.py` to bundle the Lambdas)

## Migrating from the original stack

The DB consolidation is destructive — existing per-service RDS instances and
their data go away. For a portfolio project that's fine because Flyway
recreates schemas and seeds dev data on first boot.

```powershell
cd infra/terraform

# 1. Back out the old stack first (cheapest path, avoids a confusing plan).
terraform destroy

# 2. Pull the new providers (archive, null, random).
terraform init -upgrade

# 3. Configure values.
copy terraform.tfvars.example terraform.tfvars
notepad terraform.tfvars   # set order_jwt_secret

# 4. Apply.
terraform plan
terraform apply
```

The bootstrap Lambda creates the `orders`, `inventory`, `payments` databases
on the shared instance during apply. Subsequent applies are no-ops (the
Lambda is idempotent; it only re-runs if the DB endpoint or service list
changes).

After apply, point your CI / `web-ui` at the new endpoint:

```powershell
terraform output api_endpoint
```

## Operating the scheduler

The schedules default to:

* sleep at **22:00 every day**
* wake at **08:00 Mon-Fri**

Tweak `sleep_cron`, `wake_cron`, `schedule_timezone` in `terraform.tfvars`.
To disable the scheduler entirely (keep the stack always-on):

```hcl
scheduler_enabled = false
```

Manual wake-on-demand (e.g. before an interview):

```powershell
aws lambda invoke --function-name $(terraform output -raw scheduler_lambda_name) `
  --payload '{"action":"wake"}' out.json
type out.json
```

Manual sleep:

```powershell
aws lambda invoke --function-name $(terraform output -raw scheduler_lambda_name) `
  --payload '{"action":"sleep"}' out.json
```

The Lambda is idempotent — calling `wake` on an already-running stack is
safe.

## Cost notes / known gotchas

* **Cold start after sleep**: RDS takes ~2-3 minutes to restart, ECS tasks
  another 1-2 minutes to become healthy. Wake the stack ~5 minutes before
  you demo.
* **RDS auto-restart**: AWS automatically restarts a stopped RDS instance
  after 7 days. If the sleep schedule is the only thing stopping it, that's
  fine. If you want it stopped indefinitely, disable the wake schedule.
* **Fargate Spot interruptions**: very rare in eu-west-2 for the t-shirt
  sizes we use, but possible. ECS will replace interrupted tasks
  automatically. Not appropriate for production.
* **Public IPv4 charge**: $0.005/hr per task. Three tasks * ~10hr/weekday *
  22 weekdays ~= $3.30/mo. Bounded by the scheduler.
* **CORS**: configured at the API Gateway level *and* still passed to
  `order-service` via `CORS_ALLOWED_ORIGINS`. Keep both in sync via the
  `cors_allowed_origins` variable.
