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
    namespace_id = aws_service_discovery_private_dns_namespace.main.id

    dns_records {
      type = "A"
      ttl  = 10
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
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
