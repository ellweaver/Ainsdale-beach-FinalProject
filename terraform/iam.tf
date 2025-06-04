data "aws_iam_policy_document" "trust_policy" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name_prefix        = "lambda-role"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}

data "aws_iam_policy_document" "s3_data_policy_doc" {
  statement {

    effect = "Allow"

    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket"
    ]


    resources = [
      "${aws_s3_bucket.ingestion_bucket.arn}",
      "${aws_s3_bucket.ingestion_bucket.arn}/*",
      "${aws_s3_bucket.processed_bucket.arn}",
      "${aws_s3_bucket.processed_bucket.arn}/*",
      "${aws_s3_bucket.python_bucket.arn}",
      "${aws_s3_bucket.python_bucket.arn}/*"
    ]

  }
}

resource "aws_iam_policy" "s3_write_policy" {
  name_prefix = "s3-extract-lambda_write_policy"
  policy      = data.aws_iam_policy_document.s3_data_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "lambda_s3_write_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}

data "aws_iam_policy_document" "cloudwatch_logs_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = ["*"] # may need to make this more specific
  }
}

resource "aws_iam_policy" "lambda_logging_policy" {
  name   = "lambda_logs_policy"
  policy = data.aws_iam_policy_document.cloudwatch_logs_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}


data "aws_iam_policy_document" "sns_policy" {
  statement {

    effect = "Allow"

    actions = [
      "sns:Publish"
    ]


    resources = [
      "${aws_sns_topic.sns_extract.arn}"
    ]

  }
}

data "aws_iam_policy_document" "secrets_policy" {
  statement {

    effect = "Allow"

    actions = [
      "secretsmanager:*"
    ]


    resources = [
      "*"
    ]

  }
}

resource "aws_iam_policy" "secrets_policy" {
  name_prefix = "secrets-lambda_read_policy"
  policy      = data.aws_iam_policy_document.secrets_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.secrets_policy.arn
}





resource "aws_iam_policy" "lambda_sns_policy" {
  name   = "lambda-sns-policy"
  policy = data.aws_iam_policy_document.sns_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_sns_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_sns_policy.arn
}


#iam role for step function
resource "aws_iam_role" "step_functions_role" {
    name = "ainsdale_beach_etl_step_functions_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "states.amazonaws.com"
            }
        }
        ]
    })
}


data "aws_iam_policy_document" "lambda_access_policy" {
    statement {
        effect = "Allow"
        actions = [
        "lambda:InvokeFunction"
        ]
        resources = ["arn:aws:lambda:eu-west-2:${data.aws_caller_identity.current.account_id}:function:extract_lambda_function:*"]
    }
}

data "aws_iam_policy_document" "cloudwatch_logs_eventsbridge_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogDelivery",
          "logs:GetLogDelivery",
          "logs:UpdateLogDelivery",
          "logs:DeleteLogDelivery",
          "logs:ListLogDeliveries",
          "logs:PutResourcePolicy",
          "logs:DescribeResourcePolicies",
          "logs:DescribeLogGroups"
    ]

    resources = ["*"] # may need to make this more specific
  }
}
data "aws_iam_policy_document" "step_function_logging_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams"
    ]

    resources = [
      "${aws_cloudwatch_log_group.ainsdale_beach_etl_state_machine_log.arn}:*"
    ]
  }
}
resource "aws_iam_policy" "step_function_logging_policy" {
  name="step_function_logging_policy"
  policy = data.aws_iam_policy_document.step_function_logging_policy.json
}

resource "aws_iam_role_policy_attachment" "logging_access_attachment" {
  role= aws_iam_role.step_functions_role.name
  policy_arn = aws_iam_policy.step_function_logging_policy.arn
}


resource "aws_iam_policy" "ainsdale_beach_eventsbridge_logging_policy" {
  name   = "ainsdale_beach_events_logs_policy"
  policy = data.aws_iam_policy_document.cloudwatch_logs_eventsbridge_policy.json
}

resource "aws_iam_policy" "lambda_access_policy" {
  name_prefix = "step_function_lambda_invoke_policy"
  policy      = data.aws_iam_policy_document.lambda_access_policy.json
}


resource "aws_iam_role_policy_attachment" "lambda_access_attachment" {
  role       = aws_iam_role.step_functions_role.name
  policy_arn = aws_iam_policy.lambda_access_policy.arn
}

resource "aws_iam_role_policy_attachment" "ainsdale_beach_events_bridge_policy_attachment" {
  role       = aws_iam_role.step_functions_role.name
  policy_arn = aws_iam_policy.ainsdale_beach_eventsbridge_logging_policy.arn
}

resource "aws_iam_role" "eventbridge_role" {
    name = "ainsdale_beach_etl_eventsbridge_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
            Service = "events.amazonaws.com"
            }
        }
        ]
    })
}

data "aws_iam_policy_document" "event_bridge_access_policy" {
    statement {
        effect = "Allow"
        actions = [
        "states:StartExecution"
        ]
        resources = [aws_sfn_state_machine.ainsdale_beach_etl_state_machine.arn]
    }
}

resource "aws_iam_policy" "eventbridge_access_policy" {
  name_prefix = "event_bridge_access_policy"
  policy      = data.aws_iam_policy_document.event_bridge_access_policy.json
}

resource "aws_iam_role_policy_attachment" "eventsbridge_policy_attachment" {
  role       = aws_iam_role.eventbridge_role.name
  policy_arn = aws_iam_policy.eventbridge_access_policy.arn
}