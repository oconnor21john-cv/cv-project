###############################################################################
# EventBridge Scheduler - wake / sleep the stack on a schedule
#
# Default: sleep at 22:00 weeknights and all weekend, wake at 08:00 weekdays.
# Costs: EventBridge Scheduler bills $1 per million invocations. Two daily
# triggers => effectively free.
###############################################################################

resource "aws_scheduler_schedule" "sleep" {
  name        = "${var.project_name}-sleep"
  group_name  = "default"
  description = "Scale stack to zero overnight + weekend"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = var.sleep_cron
  schedule_expression_timezone = var.schedule_timezone
  state                        = var.scheduler_enabled ? "ENABLED" : "DISABLED"

  target {
    arn      = aws_lambda_function.scheduler.arn
    role_arn = aws_iam_role.eventbridge_scheduler.arn
    input    = jsonencode({ action = "sleep" })
  }
}

resource "aws_scheduler_schedule" "wake" {
  name        = "${var.project_name}-wake"
  group_name  = "default"
  description = "Wake stack for the working day"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression          = var.wake_cron
  schedule_expression_timezone = var.schedule_timezone
  state                        = var.scheduler_enabled ? "ENABLED" : "DISABLED"

  target {
    arn      = aws_lambda_function.scheduler.arn
    role_arn = aws_iam_role.eventbridge_scheduler.arn
    input    = jsonencode({ action = "wake" })
  }
}
