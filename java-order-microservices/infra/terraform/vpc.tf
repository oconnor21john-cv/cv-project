###############################################################################
# Networking
#
# Public subnets only. No NAT Gateway (~$32/mo saved).
# Tasks live in public subnets and only run when scheduled, so the per-hour
# public IPv4 charge is bounded.
###############################################################################

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-vpc"
  })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-igw"
  })
}

resource "aws_subnet" "public" {
  for_each = tomap({
    for idx, cidr in var.public_subnet_cidrs : idx => cidr
  })

  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.value
  availability_zone       = data.aws_availability_zones.available.names[tonumber(each.key)]
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-public-${each.key}"
  })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-public-rt"
  })
}

resource "aws_route_table_association" "public_assoc" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

###############################################################################
# Security groups
###############################################################################

# Security group for the API Gateway VPC Link ENIs.
resource "aws_security_group" "vpc_link" {
  name        = "${var.project_name}-vpc-link-sg"
  description = "API Gateway VPC Link"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

# Security group for ECS tasks. Only the VPC Link SG (for order-service) and
# the VPC CIDR (for internal service-to-service traffic) can reach tasks.
resource "aws_security_group" "ecs" {
  name        = "${var.project_name}-ecs-sg"
  description = "ECS service security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "From API Gateway VPC Link to order-service"
    from_port       = 8081
    to_port         = 8081
    protocol        = "tcp"
    security_groups = [aws_security_group.vpc_link.id]
  }

  ingress {
    description = "Service-to-service inside the VPC"
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

  tags = local.common_tags
}

# Security group for the single shared RDS instance.
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-rds-sg"
  description = "RDS security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Postgres from ECS tasks"
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

  tags = local.common_tags
}
