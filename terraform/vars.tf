
variable "account_arn" {
  type    = string
  default = "arn:aws:iam::048204777974:user/Ainsdale_beach"
}

variable "python_bucket_name"{
    type=string
    default = "ainsdale-python-bucket"
}

variable "ingestion_bucket_name"{
    type=string
    default = "ainsdale-ingestion-bucket"
}

variable "processed_bucket_name"{
  type= string
  default = "ainsdale-processed-bucket"
}

variable "topic_name" {
 description = "Name of the SNS topic"
 default = "ainsdale_beach" 
}

variable "email_address" {
 description = "Email address for SNS subscription"
 default = "beachainsdale@gmail.com"
}

