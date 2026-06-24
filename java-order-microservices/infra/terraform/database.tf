###############################################################################
# Database
#
# Single db.t4g.micro Postgres instance hosting all three logical databases
# (orders, inventory, payments) instead of 3 separate db.t3.micro instances.
# Roughly $13/mo instead of $41/mo.
#
# Each service connects to its own database name with its own user; isolation
# is at the database level on a shared instance, which is fine for a portfolio
# demo. For production you would either split instances again or use Aurora.
###############################################################################

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [for subnet in aws_subnet.public : subnet.id]

  tags = local.common_tags
}

resource "random_password" "master" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_instance" "main" {
  identifier              = "${var.project_name}-shared"
  engine                  = "postgres"
  engine_version          = var.postgres_engine_version
  instance_class          = "db.t4g.micro"
  allocated_storage       = 20
  max_allocated_storage   = 50
  storage_type            = "gp3"
  username                = "appadmin"
  password                = random_password.master.result
  db_name                 = "appadmin"
  skip_final_snapshot     = true
  publicly_accessible     = false
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  backup_retention_period = 1
  apply_immediately       = true

  # Cost knobs.
  performance_insights_enabled = false
  monitoring_interval          = 0
  deletion_protection          = false

  tags = local.common_tags
}

# Build a per-service JDBC URL pointing at its database on the shared instance.
locals {
  db_url = {
    for name, svc in local.services :
    name => "jdbc:postgresql://${aws_db_instance.main.address}:5432/${svc.db_name}"
  }
}
