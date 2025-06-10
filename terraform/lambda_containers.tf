/*
resource "aws_lambda_function" "extract_lambda_container" {
  function_name = "extract_lambda_container_function"
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_role.arn
  handler       = "extract.lambda_handler"
  image_uri= "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-west-2.amazonaws.com/extract_func:0.0.1"
  package_type = "Image"

 

  timeout = 60
  publish = true
 
}
*/