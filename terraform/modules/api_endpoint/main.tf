resource "aws_s3_object" "lambda_zip" {

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/${var.lambda_zip_path}"
    source = "../../src/${var.lambda_zip_path}"

    source_hash = filesha256("../../src/${var.lambda_zip_path}")

    depends_on = [ var.s3_source_bucket ]
}

resource "aws_lambda_function" "lambda" {
    role          = var.lambda_role_arn #aws_iam_role.default_iam_role.arn

    function_name = "${var.projectName}_${var.lambda_name}"

    s3_bucket        = aws_s3_object.lambda_zip.bucket
    s3_key           = aws_s3_object.lambda_zip.key
    s3_object_version = aws_s3_object.lambda_zip.version_id

    handler       = var.lambda_handler

    runtime     = "python3.12"
    architectures = ["arm64"]
    memory_size = 128
    timeout     = 60

    tags = {
        Name = "${var.projectName}_${var.lambda_name}"
    }


    layers = var.lambda_layers
    
    environment {
      variables = var.environment_variables
    }
    
    source_code_hash = filesha256("../../src/${var.lambda_zip_path}")
    depends_on = [ var.s3_source_bucket ]
}

resource "aws_apigatewayv2_integration" "integration" {
  api_id                 = var.api_gateway_id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.lambda.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "route" {
  api_id    = var.api_gateway_id
  route_key = var.route_key
  target    = "integrations/${aws_apigatewayv2_integration.integration.id}"
}

resource "aws_lambda_permission" "allow_api" {
  statement_id  = "AllowAPIGatewayInvoke-${var.lambda_name}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_gateway_arn}/*/*"
}
