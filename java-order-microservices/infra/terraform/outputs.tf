output "alb_dns_name" {
  description = "Public DNS for order-service entrypoint."
  value       = aws_lb.main.dns_name
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
