resource "aws_cloudwatch_event_rule" "extract_lambda_schedule" {
    name = "run-extract-lambda-func-every-10-mins"
    schedule_expression = "rate(10 minutes)"
    description = "Sechudler for running the extract lamdba fucntion every ten minutes"
}

resource "aws_cloudwatch_event_target" "extract_lambda_scheduler_target" {
    rule = aws_cloudwatch_event_rule.extract_lambda_schedule.name
    target_id = "extract_lambda"
    arn = aws_lambda_function.extract_lambda.arn
}

resource "aws_lambda_permission" "extract_lambda_scheduler_permission" {
    statement_id = "AllowExecutionFromEventTrigger"
    action = "lambda:InvokeFunction"
    function_name =  aws_lambda_function.extract_lambda.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.extract_lambda_schedule.arn
  
}

