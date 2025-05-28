resource "aws_s3_bucket" "python-bucket"{
    bucket = var.python_bucket_name
    tags = {
    "description":"creation of s3 Bucket to store python functions"
}
}


resource "aws_s3_bucket" "ingestion_bucket"{
    bucket = var.ingestion_bucket_name
    tags = {
    "description":"creation of s3 Bucket to store ingested data"
}
}