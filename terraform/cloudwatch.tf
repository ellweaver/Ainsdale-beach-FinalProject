resource "aws_cloudwatch_metric_alarm" "ainsdale_beach_alarm" {
  for_each = toset(var.lambda_functions)
  alarm_name          = "AinsdaleBeach${each.key}LambdaAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 360 # 5 minutes
  statistic           = "Minimum"
  threshold           = 1 # Set your threshold value

  dimensions = { FunctionName = each.key}




  alarm_description = "Alarm when error occurs in the ainsdale beach lambda"

  actions_enabled = true

  alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:ainsdale_beach_2"]

  ok_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:ainsdale_beach_2"]
}