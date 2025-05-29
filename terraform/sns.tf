resource "aws_sns_topic" "sns_extract" {
  name            = "${var.topic_name}"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "AllowCloudWatchToPublish",
        Effect    = "Allow",
        Principal = {
          Service = "cloudwatch.amazonaws.com"
        },
        Action    = "SNS:Publish",
        Resource  = "arn:aws:sns:eu-west-2:${data.aws_caller_identity.current.account_id}:ainsdale_beach_2"
      }
    ]
  })
 
 
  delivery_policy = <<EOF
{
  "http": {
    "defaultHealthyRetryPolicy": {
      "minDelayTarget": 20,
      "maxDelayTarget": 20,
      "numRetries": 3,
      "numMaxDelayRetries": 0,
      "numNoDelayRetries": 0,
      "numMinDelayRetries": 0,
      "backoffFunction": "linear"
    },
    "disableSubscriptionOverrides": false,
    "defaultThrottlePolicy": {
      "maxReceivesPerSecond": 1
    }
  }
}
EOF
}
resource "aws_sns_topic_subscription" "email" {
  topic_arn = "${aws_sns_topic.sns_extract.arn}"
  protocol  = "email"
  endpoint  = "${var.email_address}"
}

#resource "aws_sns_topic_policy" "sns_extract_policy" {
  #arn = aws_sns_topic.sns_extract.arn
#
  #policy = data.aws_iam_policy_document.sns_extract_topic_policy.json
#}

#output "sns_topic_arn" {
  #value = "${aws_sns_topic.sns_extract.arn}"
#}

#output "sns_subscription_arn" {
 # value = "${aws_sns_topic_subscription.email.arn}"
#}

data "aws_iam_policy_document" "sns_extract_topic_policy" {
  policy_id = "__default_policy_ID"

  statement {
    actions = [
      "SNS:Subscribe",
      "SNS:SetTopicAttributes",
      "SNS:RemovePermission",
      "SNS:Receive",
      "SNS:Publish",
      "SNS:ListSubscriptionsByTopic",
      "SNS:GetTopicAttributes",
      "SNS:DeleteTopic",
      "SNS:AddPermission",
    ]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceOwner"

      values = [
        var.account_arn,
      ]
    }

    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    resources = [
    "*"
    ]

    sid = "__default_statement_ID"
  }
  
}
