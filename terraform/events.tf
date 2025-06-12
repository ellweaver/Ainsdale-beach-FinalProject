resource "aws_cloudwatch_event_rule" "ainsdale_state_machine_schedule" {
  name                = "run-step-func-every-15-mins"
  schedule_expression = "rate(15 minutes)"
  description         = "Scheduler for running the extract lamdba function every fifteen minutes"
}

resource "aws_cloudwatch_event_target" "ainsdale_etl_stepfunction" {
  rule      = aws_cloudwatch_event_rule.ainsdale_state_machine_schedule.name
  target_id = "ainsdale_etl_stepfunction"
  arn       = aws_sfn_state_machine.ainsdale_beach_etl_state_machine.arn
  role_arn = aws_iam_role.eventbridge_role.arn
}
