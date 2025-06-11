
data "archive_file" "transform_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/transform.py"
  output_path      = "${path.module}/../terraform/data/transform.zip"
}

data "archive_file" "python_utils_layer" {
  type             = "zip"
  output_file_mode = "0666"
  source_dir      = "${path.module}/../terraform/data/lambda_utils_layer"
  output_path      = "${path.module}/../terraform/data/utils_layer.zip"
  

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
  layer_name = "python_utils_layer"
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
/*
resource "aws_lambda_layer_version" "connector_x_layer" {
  s3_bucket  = "ainsdale-layers-files"
  s3_key     = "conn_x_layer.zip"
  layer_name = "python_connector_x"

}

resource "aws_lambda_layer_version" "adbc_layer" {
  s3_bucket  = "ainsdale-layers-files"
  s3_key     = "adbc_layer.zip"
  layer_name = "adbc_layer"

}
*/

resource "aws_lambda_function" "extract_lambda" {
  function_name = "extract_lambda_function"
  role          = aws_iam_role.lambda_role.arn
  image_uri= "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-west-2.amazonaws.com/extract_func:0.0.1"
  package_type = "Image"

 

  timeout = 60
  publish = true
 
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
    aws_lambda_layer_version.pyarrow_layer.arn,
  ]

  timeout = 60
  publish = true


}

resource "aws_lambda_function" "load_lambda" {
  function_name = "load_lambda_function"
  role          = aws_iam_role.lambda_role.arn
  image_uri= "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-west-2.amazonaws.com/load_func:0.0.4"
  package_type = "Image"

  

  timeout = 899
  publish = true

}
