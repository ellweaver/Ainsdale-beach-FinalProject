variable "python_bucket" {
  type    = string
  default = "ainsdale-python-bucket"
}

variable "ingestion_bucket_name" {
  type    = string
  default = "ainsdale-ingestion-bucket"
}

variable "account_arn" {
  type    = string
  default = "arn:aws:iam::048204777974:user/Ainsdale_beach"
}

variable "python_bucket_name"{
    type=string
    default = "ainsdale-python-bucket"
}

variable "processed_bucket_name"{
  type= string
  default = "ainsdale-processed-bucket"
}
