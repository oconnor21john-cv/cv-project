###############################################################################
# Image registry + service discovery + per-service async queues
###############################################################################

resource "aws_ecr_repository" "services" {
  for_each = local.services
  name     = each.key

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.common_tags
}

# Keep only the 5 most recent images per repo - cuts storage cost.
resource "aws_ecr_lifecycle_policy" "services" {
  for_each   = aws_ecr_repository.services
  repository = each.value.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 5 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      }
      action = { type = "expire" }
    }]
  })
}

resource "aws_service_discovery_private_dns_namespace" "main" {
  name = "${var.project_name}.local"
  vpc  = aws_vpc.main.id
  tags = local.common_tags
}

resource "aws_service_discovery_service" "services" {
  for_each = local.services
  name     = each.key

  dns_config {
    namespace_id   = aws_service_discovery_private_dns_namespace.main.id
    routing_policy = "MULTIVALUE"

    # A records for inter-service HTTP calls within the VPC.
    dns_records {
      type = "A"
      ttl  = 10
    }

    # SRV records carry the port - required by API Gateway HTTP API VPC Link
    # integrations targeting Cloud Map. Without them the integration defaults
    # to port 80 and the upstream connect fails with a 500.
    dns_records {
      type = "SRV"
      ttl  = 10
    }
  }

  # No health_check_custom_config: that requires ECS to actively report
  # health, which it only does with a task healthCheck block. Without one,
  # instances would stay UNHEALTHY forever.
}

resource "aws_cloudwatch_log_group" "services" {
  for_each          = local.services
  name              = "/ecs/${var.project_name}/${each.key}"
  retention_in_days = 7
  tags              = local.common_tags
}

resource "aws_sqs_queue" "services" {
  for_each                  = local.services
  name                      = "${var.project_name}-${each.key}-events"
  message_retention_seconds = 86400 # 1 day, was the AWS default 4 days

  tags = local.common_tags
}
