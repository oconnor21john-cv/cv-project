# AWS Terraform Bootstrap

This stack provisions a practical starter environment for your three Java microservices:

- ECR repositories: `order-service`, `inventory-service`, `payment-service`
- ECS Fargate cluster + one ECS service per microservice
- ALB exposing `order-service` publicly
- Cloud Map internal DNS for service-to-service calls
- One SQS queue per service for async event publishing
- One Postgres RDS instance per service
- Secrets Manager for DB passwords + JWT secret

## 1) Prerequisites

- Terraform `>= 1.6`
- AWS CLI configured (`aws configure`)

## 2) Configure values

```powershell
cd infra/terraform
copy terraform.tfvars.example terraform.tfvars
```

Update `terraform.tfvars` with real values, especially:

- `order_jwt_secret`
- `db_passwords`

## 3) Deploy infrastructure

```powershell
terraform init
terraform plan
terraform apply
```

Save outputs after apply:

```powershell
terraform output
```

You will need:

- `ecs_cluster_name` for GitHub Actions
- `alb_dns_name` to call the public API

## 4) Push initial images

The GitHub Actions workflow in `.github/workflows/deploy-ecs.yml` handles regular builds/deploys after your first push to GitHub.

## 5) Important notes

- This is a **starter** stack optimized for getting live quickly.
- For production, move ECS tasks and RDS to private subnets with NAT, add HTTPS (ACM), WAF, autoscaling, and Multi-AZ database settings.
