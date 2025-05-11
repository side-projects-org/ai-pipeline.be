module "api_get_sample_model_by_key" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage=var.stage

  lambda_name     = "api_get_sample_model_by_key"
  lambda_handler  = "api.sample.api_get_sample_model_by_key.api_get_sample_model_by_key.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/sample/api_get_sample_model_by_key/build.zip"

  lambda_layers = [
        aws_lambda_layer_version.layer_library_common_version.arn,
        aws_lambda_layer_version.layer_common_version.arn,
    ]

  environment_variables = {
      project_name = var.projectName
      stage_name   = var.stage
  }

  api_gateway_id  = aws_apigatewayv2_api.http_api.id
  api_gateway_arn = aws_apigatewayv2_api.http_api.execution_arn
  route_key       = "GET /sample"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}
