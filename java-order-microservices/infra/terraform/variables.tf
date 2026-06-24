variable "project_name" {
  description = "Project name prefix."
  type        = string
  default     = "java-order-ms"
}

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "eu-west-2"
}

variable "vpc_cidr" {
  description = "CIDR range for the VPC."
  type        = string
  default     = "10.42.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Two public subnet CIDRs in different AZs."
  type        = list(string)
  default     = ["10.42.1.0/24", "10.42.2.0/24"]
}

variable "order_jwt_secret" {
  description = "JWT secret for order-service (32+ chars recommended)."
  type        = string
  sensitive   = true
}

variable "ecs_task_cpu" {
  description = "CPU units per ECS task."
  type        = number
  default     = 512
}

variable "ecs_task_memory" {
  description = "Memory in MiB per ECS task."
  type        = number
  default     = 1024
}

variable "postgres_engine_version" {
  description = "Postgres engine version for the shared RDS instance."
  type        = string
  # Matches what the old per-service instances were running. Set this to the
  # latest minor offered in your region if you want fresher patches.
  default = "18.3"
}

variable "cors_allowed_origins" {
  description = "Comma-separated list of origins permitted by the API Gateway + order-service CORS config."
  type        = string
  default     = "https://johnoconnor-cv.vercel.app,https://cv-johnoconnor.netlify.app,http://localhost:5173"
}

variable "scheduler_enabled" {
  description = "Toggle the sleep/wake EventBridge schedules. Disable to keep the stack always-on."
  type        = bool
  default     = true
}

variable "sleep_cron" {
  description = "cron(min hr day-of-month month day-of-week year) — when to scale to zero."
  type        = string
  # 22:00 every day in the configured timezone.
  default = "cron(0 22 * * ? *)"
}

variable "wake_cron" {
  description = "cron(min hr day-of-month month day-of-week year) — when to scale back up."
  type        = string
  # 08:00 Mon-Fri in the configured timezone.
  default = "cron(0 8 ? * MON-FRI *)"
}

variable "schedule_timezone" {
  description = "IANA timezone for sleep/wake schedules."
  type        = string
  default     = "Europe/London"
}
