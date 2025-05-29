
data "archive_file" "extract_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/extract.py"
  output_path      = "${path.module}/../terraform/data/extract.zip"
}

data "archive_file" "load_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/load.py"
  output_path      = "${path.module}/../terraform/data/load.zip"
}

data "archive_file" "transform_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/transform.py"
  output_path      = "${path.module}/../terraform/data/transform.zip"
}

data "archive_file" "utils_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../utils/utils.py"
  output_path      = "${path.module}/../terraform/data/utils.zip"
}

resource "aws_s3_object" "extract_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "extract_func"
  source = data.archive_file.extract_py.output_path
  etag = filemd5( data.archive_file.extract_py.output_path)
}

resource "aws_s3_object" "load_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "load_func"
  source = data.archive_file.load_py.output_path
  etag = filemd5( data.archive_file.load_py.output_path)
  
}

resource "aws_s3_object" "transform_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "transform_func"
  source = data.archive_file.transform_py.output_path
  etag = filemd5( data.archive_file.transform_py.output_path)
  
}

resource "aws_s3_object" "utils_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "utils_func"
  source = data.archive_file.utils_py.output_path
  etag = filemd5( data.archive_file.utils_py.output_path)

}

resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_lambda_function"
  runtime = "python3.11"
  role = aws_iam_role.extract_lambda_role.arn
  handler = "extract.lambda_handler"

  s3_bucket = aws_s3_bucket.python_bucket.bucket
  s3_key = aws_s3_object.extract_file_upload.key
  

  timeout = 60
  publish = true
  
  environment {
    variables = {
      SECRET_NAME = "toteys_db_credentials"
    }
  }
}


