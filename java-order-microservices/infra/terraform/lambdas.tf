###############################################################################
# Lambda functions
#
# Both Lambdas share one zip artifact (pg8000 is small; bundling once keeps
# Terraform tidy and avoids two build passes).
###############################################################################

resource "null_resource" "lambda_build" {
  triggers = {
    handler_db   = filesha256("${path.module}/lambda/db_bootstrap.py")
    handler_sch  = filesha256("${path.module}/lambda/scheduler.py")
    builder      = filesha256("${path.module}/lambda/build.py")
  }

  provisioner "local-exec" {
    # Set working_dir so we can use a quote-free relative path - avoids
    # Windows cmd.exe escape issues when path.module contains spaces.
    working_dir = path.module
    command     = "python lambda/build.py"
    on_failure  = fail
  }
}

data "archive_file" "lambda_package" {
  depends_on  = [null_resource.lambda_build]
  type        = "zip"
  source_dir  = "${path.module}/lambda/build"
  output_path = "${path.module}/lambda/lambda.zip"
}

# Security group for Lambdas that need VPC access (db_bootstrap only).
resource "aws_security_group" "lambda" {
  name        = "${var.project_name}-lambda-sg"
  description = "Lambda functions needing VPC access"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

# RDS must accept Postgres traffic from the Lambda SG as well as ECS.
resource "aws_security_group_rule" "rds_from_lambda" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.lambda.id
  security_group_id        = aws_security_group.rds.id
  description              = "Postgres from bootstrap Lambda"
}

###############################################################################
# DB bootstrap Lambda - creates the per-service databases on first apply.
###############################################################################

resource "aws_lambda_function" "db_bootstrap" {
  function_name    = "${var.project_name}-db-bootstrap"
  role             = aws_iam_role.lambda_bootstrap.arn
  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  handler          = "db_bootstrap.handler"
  runtime          = "python3.12"
  timeout          = 60
  memory_size      = 256

  environment {
    variables = {
      DB_HOST     = aws_db_instance.main.address
      DB_PORT     = tostring(aws_db_instance.main.port)
      DB_USER     = aws_db_instance.main.username
      DB_NAME     = aws_db_instance.main.db_name
      DB_PASSWORD = random_password.master.result
      DATABASES   = jsonencode([for s in local.services : s.db_name])
    }
  }

  vpc_config {
    subnet_ids         = [for subnet in aws_subnet.public : subnet.id]
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = local.common_tags
}

# Invoke the bootstrap on every apply. The Lambda is idempotent, and any
# change to db_endpoint or the database catalogue changes the `input`,
# which forces Terraform to re-invoke.
resource "aws_lambda_invocation" "db_bootstrap" {
  depends_on    = [aws_secretsmanager_secret_version.db_master]
  function_name = aws_lambda_function.db_bootstrap.function_name

  input = jsonencode({
    db_endpoint = aws_db_instance.main.endpoint
    databases   = [for s in local.services : s.db_name]
  })
}

###############################################################################
# Scheduler Lambda - wakes / sleeps the stack.
###############################################################################

resource "aws_lambda_function" "scheduler" {
  function_name    = "${var.project_name}-scheduler"
  role             = aws_iam_role.lambda_scheduler.arn
  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256
  handler          = "scheduler.handler"
  runtime          = "python3.12"
  timeout          = 60
  memory_size      = 128

  environment {
    variables = {
      ECS_CLUSTER             = aws_ecs_cluster.main.name
      DB_INSTANCE_IDENTIFIER  = aws_db_instance.main.identifier
      SERVICES                = jsonencode({ for k, _ in local.services : k => 1 })
    }
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "scheduler" {
  name              = "/aws/lambda/${aws_lambda_function.scheduler.function_name}"
  retention_in_days = 7
  tags              = local.common_tags
}

resource "aws_cloudwatch_log_group" "db_bootstrap" {
  name              = "/aws/lambda/${aws_lambda_function.db_bootstrap.function_name}"
  retention_in_days = 7
  tags              = local.common_tags
}
