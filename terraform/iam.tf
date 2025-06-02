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

resource "aws_iam_role" "extract_lambda_role" {
  name_prefix        = "lambda-extract-role"
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
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}

data "aws_iam_policy_document" "extract_lambda_logs_policy" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = ["arn:aws:logs:*:*:*"] # may need to make this more specific
  }
}

resource "aws_iam_policy" "extract_logging_policy" {
  name   = "extract-lambda_logs_policy"
  policy = data.aws_iam_policy_document.extract_lambda_logs_policy.json
}

resource "aws_iam_role_policy_attachment" "extract_lambda_logs_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.extract_logging_policy.arn
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
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.secrets_policy.arn
}





resource "aws_iam_policy" "extract_lambda_sns_policy" {
  name   = "extract-lambda-sns-policy"
  policy = data.aws_iam_policy_document.sns_policy.json
}

resource "aws_iam_role_policy_attachment" "extract_lambda_sns_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.extract_lambda_sns_policy.arn
}
