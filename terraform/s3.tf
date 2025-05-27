resource "aws_s3_bucket""python-bucket"{
    bucket = var.python_bucket
    tags = {
    "description":"creation of s3 Bucket to store python functions"
}
}