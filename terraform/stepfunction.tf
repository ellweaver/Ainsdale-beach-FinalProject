
resource "aws_cloudwatch_log_group" "ainsdale_beach_etl_state_machine_log" {
  name = "ainsdale_beach_etl_state_machine_log" 
}

resource "aws_sfn_state_machine" "ainsdale_beach_etl_state_machine" {
  name     = "ainsdale_beach_etl_state_machine"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = <<EOF
  {
  "Comment": "A description of my state machine",
  "StartAt": "extract Lambda invokation",
  "States": {
    "extract Lambda invokation": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:eu-west-2:${data.aws_caller_identity.current.account_id}:function:extract_lambda_function:$LATEST",
        "Payload": "{% $states.input %}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "QueryLanguage": "JSONata"
}

EOF


  logging_configuration {
    log_destination        = "${aws_cloudwatch_log_group.ainsdale_beach_etl_state_machine_log.arn}:*"
    include_execution_data = true
    level                  = "ALL"
  }
}




