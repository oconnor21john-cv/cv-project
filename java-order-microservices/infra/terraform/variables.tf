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

variable "db_passwords" {
  description = "DB passwords per service."
  type = object({
    orders    = string
    inventory = string
    payments  = string
  })
  sensitive = true
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
