###############################################################################
# Public ingress: API Gateway HTTP API + VPC Link
#
# Replaces the ALB ($16/mo idle). HTTP APIs are billed per request only - for
# a portfolio with effectively zero traffic the spend is fractions of a cent
# per month. VPC Link integration targets the order-service Cloud Map record
# directly (no NLB needed).
###############################################################################

resource "aws_apigatewayv2_vpc_link" "main" {
  name               = "${var.project_name}-vpc-link"
  security_group_ids = [aws_security_group.vpc_link.id]
  subnet_ids         = [for subnet in aws_subnet.public : subnet.id]

  tags = local.common_tags
}

resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = split(",", var.cors_allowed_origins)
    allow_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    allow_headers = ["authorization", "content-type", "x-correlation-id"]
    max_age       = 300
  }

  tags = local.common_tags
}

resource "aws_apigatewayv2_integration" "order_service" {
  api_id           = aws_apigatewayv2_api.main.id
  integration_type = "HTTP_PROXY"

  integration_uri    = aws_service_discovery_service.services["order-service"].arn
  integration_method = "ANY"
  connection_type    = "VPC_LINK"
  connection_id      = aws_apigatewayv2_vpc_link.main.id

  payload_format_version = "1.0"
  timeout_milliseconds   = 29000
}

# Catch-all route. order-service is responsible for routing /auth/*, /orders/*,
# /actuator/health etc internally.
resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.order_service.id}"
}

# Explicit root route so GET / returns something instead of a 404.
resource "aws_apigatewayv2_route" "root" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.order_service.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true

  # Throttling caps to avoid surprise bills under a misconfigured client.
  default_route_settings {
    throttling_burst_limit = 50
    throttling_rate_limit  = 25
  }

  tags = local.common_tags
}
