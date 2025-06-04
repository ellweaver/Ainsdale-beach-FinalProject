
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

data "archive_file" "python_utils_layer" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir       = "${path.module}/data/lambda_utils_layer"
  output_path      = "${path.module}/../terraform/data/lambda_utils_layer.zip"
}



resource "aws_s3_object" "extract_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "extract_func"
  source = data.archive_file.extract_py.output_path
  etag   = filemd5(data.archive_file.extract_py.output_path)
}

resource "aws_s3_object" "load_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "load_func"
  source = data.archive_file.load_py.output_path
  etag   = filemd5(data.archive_file.load_py.output_path)

}

resource "aws_s3_object" "transform_file_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "transform_func"
  source = data.archive_file.transform_py.output_path
  etag   = filemd5(data.archive_file.transform_py.output_path)

}

resource "aws_s3_object" "python_utils_layer_upload" {
  bucket = aws_s3_bucket.python_bucket.bucket
  key    = "python_utils"
  source = data.archive_file.python_utils_layer.output_path
  etag   = filemd5(data.archive_file.python_utils_layer.output_path)

}

resource "aws_lambda_layer_version" "python_utils_layer" {
  s3_bucket  = aws_s3_bucket.python_bucket.bucket
  s3_key     = aws_s3_object.python_utils_layer_upload.key
  layer_name = "python_utils"

}

resource "aws_lambda_layer_version" "python_pg8000_layer" {
  s3_bucket  = "ainsdale-layers-files"
  s3_key     = "lambda_pg8000_layer.zip"
  layer_name = "python_pg8000"

}

resource "aws_lambda_layer_version" "python_polars_layer" {
  s3_bucket  = "ainsdale-layers-files"
  s3_key     = "lambda_polars_layer.zip"
  layer_name = "python_polars"

}

resource "aws_lambda_layer_version" "pyarrow_layer" {
  s3_bucket  = "ainsdale-layers-files"
  s3_key     = "pyarrow_layer.zip"
  layer_name = "python_pyarrow"

}


resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_lambda_function"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_role.arn
  handler       = "extract.lambda_handler"

  s3_bucket = aws_s3_bucket.python_bucket.bucket
  s3_key    = aws_s3_object.extract_file_upload.key
  source_code_hash=data.archive_file.extract_py.output_base64sha256
  layers = [
    aws_lambda_layer_version.python_utils_layer.arn,
    aws_lambda_layer_version.python_pg8000_layer.arn,
    aws_lambda_layer_version.python_polars_layer.arn,
  ]

  timeout = 60
  publish = true

  environment {
    variables = {
      SECRET_NAME = "toteys_db_credentials"
    }
  }
}

resource "aws_lambda_function" "transform_lambda" {
  function_name = "transform_lambda_function"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_role.arn
  handler       = "transform.lambda_handler"

  s3_bucket = aws_s3_bucket.python_bucket.bucket
  s3_key    = aws_s3_object.transform_file_upload.key
  source_code_hash=data.archive_file.transform_py.output_base64sha256
  layers = [
    aws_lambda_layer_version.python_utils_layer.arn,
    aws_lambda_layer_version.python_polars_layer.arn,
    aws_lambda_layer_version.pyarrow_layer.arn
  ]

  timeout = 60
  publish = true

  environment {
    variables = {
      SECRET_NAME = "toteys_db_credentials"
    }
  }
}

resource "aws_lambda_function" "load_lambda" {
  function_name = "load_lambda_function"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_role.arn
  handler       = "load.lambda_handler"

  s3_bucket = aws_s3_bucket.python_bucket.bucket
  s3_key    = aws_s3_object.load_file_upload.key
  source_code_hash=data.archive_file.load_py.output_base64sha256
  layers = [
    aws_lambda_layer_version.python_utils_layer.arn,
    aws_lambda_layer_version.python_polars_layer.arn,
    aws_lambda_layer_version.pyarrow_layer.arn
  ]

  timeout = 60
  publish = true

  environment {
    variables = {
      SECRET_NAME = "toteys_db_credentials"
    }
  }
}