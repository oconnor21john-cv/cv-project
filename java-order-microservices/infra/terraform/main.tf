provider "aws" {
  region = var.aws_region
}

locals {
  services = {
    order-service = {
      port          = 8081
      db_name       = "orders"
      db_user       = "orders"
      db_secret_key = "orders"
    }
    inventory-service = {
      port          = 8082
      db_name       = "inventory"
      db_user       = "inventory"
      db_secret_key = "inventory"
    }
    payment-service = {
      port          = 8083
      db_name       = "payments"
      db_user       = "payments"
      db_secret_key = "payments"
    }
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

resource "aws_subnet" "public" {
  for_each = tomap({
    for idx, cidr in var.public_subnet_cidrs : idx => cidr
  })

  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.value
  availability_zone       = data.aws_availability_zones.available.names[tonumber(each.key)]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-${each.key}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

resource "aws_route_table_association" "public_assoc" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_ecr_repository" "services" {
  for_each = local.services
  name     = each.key

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"
}

resource "aws_service_discovery_private_dns_namespace" "main" {
  name = "${var.project_name}.local"
  vpc  = aws_vpc.main.id
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
  }
}

resource "aws_cloudwatch_log_group" "services" {
  for_each          = local.services
  name              = "/ecs/${var.project_name}/${each.key}"
  retention_in_days = 14
}

resource "aws_sqs_queue" "services" {
  for_each = local.services
  name     = "${var.project_name}-${each.key}-events"
}

resource "aws_secretsmanager_secret" "db" {
  for_each = local.services
  name     = "${var.project_name}/${each.key}/db"
}

resource "aws_secretsmanager_secret_version" "db" {
  for_each      = local.services
  secret_id     = aws_secretsmanager_secret.db[each.key].id
  secret_string = jsonencode({ password = var.db_passwords[each.value.db_secret_key] })
}

resource "aws_secretsmanager_secret" "order_jwt" {
  name = "${var.project_name}/order-service/jwt"
}

resource "aws_secretsmanager_secret_version" "order_jwt" {
  secret_id     = aws_secretsmanager_secret.order_jwt.id
  secret_string = jsonencode({ jwt_secret = var.order_jwt_secret })
}

resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "ALB security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "ecs" {
  name        = "${var.project_name}-ecs-sg"
  description = "ECS service security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 8081
    to_port     = 8083
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "RDS security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [for subnet in aws_subnet.public : subnet.id]
}

resource "aws_db_instance" "services" {
  for_each = local.services

  identifier              = "${var.project_name}-${each.value.db_name}"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  username                = each.value.db_user
  password                = var.db_passwords[each.value.db_secret_key]
  db_name                 = each.value.db_name
  skip_final_snapshot     = true
  publicly_accessible     = false
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  backup_retention_period = 1
}

resource "aws_iam_role" "ecs_execution_role" {
  name = "${var.project_name}-ecs-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_policy" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "ecs_execution_secrets_policy" {
  name = "${var.project_name}-ecs-exec-secrets"
  role = aws_iam_role.ecs_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue", "kms:Decrypt"]
      Resource = ["*"]
    }]
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${var.project_name}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "ecs_task_sqs_policy" {
  name = "${var.project_name}-ecs-task-sqs"
  role = aws_iam_role.ecs_task_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["sqs:SendMessage"]
      Resource = [
        for queue in aws_sqs_queue.services : queue.arn
      ]
    }]
  })
}

resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [for subnet in aws_subnet.public : subnet.id]
}

resource "aws_lb_target_group" "order" {
  name        = "${var.project_name}-order-tg"
  port        = 8081
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = "/actuator/health"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    interval            = 30
    timeout             = 10
    matcher             = "200"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.order.arn
  }
}

resource "aws_ecs_task_definition" "services" {
  for_each = local.services

  family                   = "${var.project_name}-${each.key}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

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
          { name = "SPRING_DATASOURCE_URL", value = "jdbc:postgresql://${aws_db_instance.services[each.key].address}:5432/${each.value.db_name}" },
          { name = "SPRING_DATASOURCE_USERNAME", value = each.value.db_user },
          { name = "APP_SQS_ENABLED", value = "true" }
        ],
        each.key == "order-service" ? [
          { name = "INVENTORY_BASE_URL", value = "http://inventory-service.${aws_service_discovery_private_dns_namespace.main.name}:8082" },
          { name = "PAYMENT_BASE_URL", value = "http://payment-service.${aws_service_discovery_private_dns_namespace.main.name}:8083" },
          { name = "APP_SQS_QUEUE_ORDERS_URL", value = aws_sqs_queue.services["order-service"].url },
          { name = "CORS_ALLOWED_ORIGINS", value = "https://johnoconnor-cv.vercel.app,https://cv-johnoconnor.netlify.app,http://localhost:5173" }
        ] : each.key == "inventory-service" ? [
          { name = "APP_SQS_QUEUE_INVENTORY_URL", value = aws_sqs_queue.services["inventory-service"].url }
        ] : each.key == "payment-service" ? [
          { name = "APP_SQS_QUEUE_PAYMENTS_URL", value = aws_sqs_queue.services["payment-service"].url }
        ] : []
      )
      secrets = concat(
        [
          { name = "SPRING_DATASOURCE_PASSWORD", valueFrom = "${aws_secretsmanager_secret.db[each.key].arn}:password::" }
        ],
        each.key == "order-service" ? [
          { name = "JWT_SECRET", valueFrom = "${aws_secretsmanager_secret.order_jwt.arn}:jwt_secret::" }
        ] : []
      )
    }
  ])
}

resource "aws_ecs_service" "services" {
  for_each = local.services

  name                               = each.key
  cluster                            = aws_ecs_cluster.main.id
  task_definition                    = aws_ecs_task_definition.services[each.key].arn
  desired_count                      = 1
  launch_type                        = "FARGATE"
  health_check_grace_period_seconds  = each.key == "order-service" ? 180 : null

  network_configuration {
    subnets          = [for subnet in aws_subnet.public : subnet.id]
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  service_registries {
    registry_arn = aws_service_discovery_service.services[each.key].arn
  }

  dynamic "load_balancer" {
    for_each = each.key == "order-service" ? [1] : []
    content {
      target_group_arn = aws_lb_target_group.order.arn
      container_name   = each.key
      container_port   = each.value.port
    }
  }
}
