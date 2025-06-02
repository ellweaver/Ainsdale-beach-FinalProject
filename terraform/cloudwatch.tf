resource "aws_cloudwatch_metric_alarm" "ainsdale_beach_alarm" {
  alarm_name          = "AinsdaleBeachLambdaAlarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300 # 5 minutes
  statistic           = "Minimum"
  threshold           = 1 # Set your threshold value

  dimensions = { FunctionName = aws_lambda_function.extract_lambda.function_name }


  alarm_description = "Alarm when error occurs in the ainsdale beach lambda"

  actions_enabled = true

  alarm_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:ainsdale_beach_2"]

  ok_actions = ["arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:ainsdale_beach_2"]
}