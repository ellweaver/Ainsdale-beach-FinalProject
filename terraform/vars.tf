/*
variable "account_arn" {
  type    = string
  default = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/Ainsdale_beach"
}
*/
variable "python_bucket_name" {
  type    = string
  default = "ainsdale-python-bucket-2"
}

variable "ingestion_bucket_name" {
  type    = string
  default = "ainsdale-ingestion-bucket"
}

variable "processed_bucket_name" {
  type    = string
  default = "ainsdale-processed-bucket"
}

variable "topic_name" {
  description = "Name of the SNS topic"
  default     = "ainsdale_beach_2"
}

variable "email_address" {
  description = "Email address for SNS subscription"
  default     = "beachainsdale@gmail.com"
}

variable "lambda_functions" {
  type = list(string)
  default = [ "extract_lambda_function", "transform_lambda_function",
  "load_lambda_function" ]
}
