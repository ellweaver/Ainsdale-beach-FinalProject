resource "aws_s3_bucket" "python_bucket"{
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

resource "aws_s3_bucket" "processed_bucket"{
    bucket = var.processed_bucket_name
    tags = {
        "description": "creation of S3 bucket to store processed data"
    }
}