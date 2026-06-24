output "api_endpoint" {
  description = "Public API Gateway endpoint (replaces alb_dns_name)."
  value       = aws_apigatewayv2_api.main.api_endpoint
}

output "ecs_cluster_name" {
  description = "ECS cluster name for CI deploys."
  value       = aws_ecs_cluster.main.name
}

output "ecr_repository_urls" {
  description = "ECR repository URLs by service."
  value       = { for k, v in aws_ecr_repository.services : k => v.repository_url }
}

output "sqs_queue_urls" {
  description = "SQS queue URLs by service."
  value       = { for k, v in aws_sqs_queue.services : k => v.url }
}

output "db_endpoint" {
  description = "Shared Postgres endpoint."
  value       = aws_db_instance.main.endpoint
}

output "db_master_secret_arn" {
  description = "Secrets Manager ARN holding the master DB credentials."
  value       = aws_secretsmanager_secret.db_master.arn
}

output "scheduler_lambda_name" {
  description = "Lambda function that wakes/sleeps the stack — invoke with {\"action\":\"wake\"} or {\"action\":\"sleep\"}."
  value       = aws_lambda_function.scheduler.function_name
}
