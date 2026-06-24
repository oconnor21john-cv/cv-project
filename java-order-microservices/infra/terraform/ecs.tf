###############################################################################
# ECS cluster + services on Fargate Spot
#
# Fargate Spot is ~70% cheaper than on-demand Fargate. Tasks can be reclaimed
# with 2 minutes notice, which is fine for a portfolio demo. We pin 100% of
# capacity to Spot to maximise savings.
###############################################################################

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled" # Container Insights is ~$1.50/cluster/mo, not needed here.
  }

  tags = local.common_tags
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 100
    base              = 0
  }
}

###############################################################################
# Task definitions
###############################################################################

resource "aws_ecs_task_definition" "services" {
  for_each = local.services

  family                   = "${var.project_name}-${each.key}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name      = each.key
      image     = "${aws_ecr_repository.services[each.key].repository_url}:latest"
      essential = true

      portMappings = [{
        containerPort = each.value.port
        hostPort      = each.value.port
        protocol      = "tcp"
      }]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.services[each.key].name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }

      environment = concat(
        [
          { name = "SERVER_PORT", value = tostring(each.value.port) },
          { name = "SPRING_DATASOURCE_URL", value = local.db_url[each.key] },
          { name = "SPRING_DATASOURCE_USERNAME", value = aws_db_instance.main.username },
          { name = "APP_SQS_ENABLED", value = "true" },
        ],
        each.key == "order-service" ? [
          { name = "INVENTORY_BASE_URL", value = "http://inventory-service.${aws_service_discovery_private_dns_namespace.main.name}:8082" },
          { name = "PAYMENT_BASE_URL", value = "http://payment-service.${aws_service_discovery_private_dns_namespace.main.name}:8083" },
          { name = "APP_SQS_QUEUE_ORDERS_URL", value = aws_sqs_queue.services["order-service"].url },
          { name = "CORS_ALLOWED_ORIGINS", value = var.cors_allowed_origins },
        ] : each.key == "inventory-service" ? [
          { name = "APP_SQS_QUEUE_INVENTORY_URL", value = aws_sqs_queue.services["inventory-service"].url },
        ] : each.key == "payment-service" ? [
          { name = "APP_SQS_QUEUE_PAYMENTS_URL", value = aws_sqs_queue.services["payment-service"].url },
        ] : []
      )

      secrets = concat(
        [
          { name = "SPRING_DATASOURCE_PASSWORD", valueFrom = "${aws_secretsmanager_secret.db_master.arn}:password::" },
        ],
        each.key == "order-service" ? [
          { name = "JWT_SECRET", valueFrom = aws_ssm_parameter.jwt_secret.arn },
        ] : []
      )
    }
  ])

  tags = local.common_tags
}

###############################################################################
# Services. desired_count is left at 1 here but EventBridge Scheduler will
# bounce it to 0 overnight via the scheduler Lambda. `ignore_changes` keeps
# Terraform from fighting the scheduler.
###############################################################################

resource "aws_ecs_service" "services" {
  for_each = local.services

  name            = each.key
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.services[each.key].arn
  desired_count   = 1

  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 100
    base              = 0
  }

  network_configuration {
    subnets          = [for subnet in aws_subnet.public : subnet.id]
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  service_registries {
    registry_arn = aws_service_discovery_service.services[each.key].arn
  }

  health_check_grace_period_seconds = each.key == "order-service" ? 180 : null

  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 200

  lifecycle {
    ignore_changes = [desired_count]
  }

  depends_on = [aws_lambda_invocation.db_bootstrap]

  tags = local.common_tags
}
