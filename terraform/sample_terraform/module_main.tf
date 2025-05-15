module "api_get_prompt_model_list" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage=var.stage

  lambda_name     = "api_get_prompt_model_list"
  lambda_handler  = "api.prompt.api_get_prompt_model_list.api_get_prompt_model_list.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/prompt/api_get_prompt_model_list/build.zip"

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
  route_key       = "GET /prompt"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}
