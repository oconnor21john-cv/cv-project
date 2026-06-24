provider "aws" {
  region = var.aws_region
}

# Shared service catalog. Adjust ports / db names here, downstream files read this map.
locals {
  services = {
    order-service = {
      port    = 8081
      db_name = "orders"
      db_user = "orders"
    }
    inventory-service = {
      port    = 8082
      db_name = "inventory"
      db_user = "inventory"
    }
    payment-service = {
      port    = 8083
      db_name = "payments"
      db_user = "payments"
    }
  }

  # Tags applied to every resource.
  common_tags = {
    Project = var.project_name
    Stack   = "cost-optimized"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
