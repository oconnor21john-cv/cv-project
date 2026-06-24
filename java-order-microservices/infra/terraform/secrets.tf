###############################################################################
# Secrets / parameters
#
# DB master password lives in a single Secrets Manager entry (needed by the
# bootstrap Lambda, which only supports Secrets Manager IAM resource policies
# cleanly). The JWT secret lives in SSM Parameter Store SecureString (free).
#
# Net change vs the original stack: 4 Secrets Manager entries -> 1, saving
# roughly $1.20/mo.
###############################################################################

resource "aws_secretsmanager_secret" "db_master" {
  name                    = "${var.project_name}/db/master"
  description             = "Master password for the shared Postgres instance"
  recovery_window_in_days = 0
  tags                    = local.common_tags
}

resource "aws_secretsmanager_secret_version" "db_master" {
  secret_id = aws_secretsmanager_secret.db_master.id
  secret_string = jsonencode({
    username = aws_db_instance.main.username
    password = random_password.master.result
  })
}

resource "aws_ssm_parameter" "jwt_secret" {
  name        = "/${var.project_name}/order-service/jwt-secret"
  description = "JWT signing secret for order-service"
  type        = "SecureString"
  value       = var.order_jwt_secret
  tags        = local.common_tags
}
