
data "archive_file" "extract_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/extract.py"
  output_path      = "${path.module}/../terraform/extract.zip"
}

data "archive_file" "load_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/load.py"
  output_path      = "${path.module}/../terraform/load.zip"
}

data "archive_file" "transform_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../src/transform.py"
  output_path      = "${path.module}/../terraform/transform.zip"
}

data "archive_file" "utils_py" {
  type             = "zip"
  output_file_mode = "0666"
  source_file      = "${path.module}/../utils/utils.py"
  output_path      = "${path.module}/../terraform/utils.zip"
}

resource "aws_s3_object" "extract_file_upload" {
  bucket = var.python_bucket
  key    = "extract_func"
  source = data.archive_file.extract_py.output_path
  etag = filemd5( data.archive_file.extract_py.output_path)
}

resource "aws_s3_object" "load_file_upload" {
  bucket = var.python_bucket
  key    = "load_func"
  source = data.archive_file.load_py.output_path
  etag = filemd5( data.archive_file.load_py.output_path)
}

resource "aws_s3_object" "transform_file_upload" {
  bucket = var.python_bucket
  key    = "transform_func"
  source = data.archive_file.transform_py.output_path
  etag = filemd5( data.archive_file.transform_py.output_path)
}

resource "aws_s3_object" "utils_file_upload" {
  bucket = var.python_bucket
  key    = "utils_func"
  source = data.archive_file.utils_py.output_path
  etag = filemd5( data.archive_file.utils_py.output_path)
}
