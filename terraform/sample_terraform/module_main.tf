module "api_get_prompt_model_list" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage       = var.stage

  lambda_name     = "api_get_prompt_model_list"
  lambda_handler  = "api.prompt.api_get_prompt_model_list.api_get_prompt_model_list.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/prompt/api_get_prompt_model_list/build.zip"

  lambda_layers = [
    aws_lambda_layer_version.layer_library_common_version.arn,
    aws_lambda_layer_version.layer_common_version.arn,
  ]

  environment_variables = {
    PROJECT_NAME = var.projectName
    STAGE_NAME   = var.stage
    OPEN_AI_KEY = var.openAIKey
  }

  api_gateway_id   = aws_apigatewayv2_api.http_api.id
  api_gateway_arn  = aws_apigatewayv2_api.http_api.execution_arn
  route_key        = "GET /prompt"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}
module "api_put_prompt_model" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage       = var.stage

  lambda_name     = "api_put_prompt_model"
  lambda_handler  = "api.prompt.api_put_prompt_model.api_put_prompt_model.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/prompt/api_put_prompt_model/build.zip"

  lambda_layers = [
    aws_lambda_layer_version.layer_library_common_version.arn,
    aws_lambda_layer_version.layer_common_version.arn,
  ]

  environment_variables = {
    PROJECT_NAME = var.projectName
    STAGE_NAME   = var.stage
    OPEN_AI_KEY = var.openAIKey
  }

  api_gateway_id   = aws_apigatewayv2_api.http_api.id
  api_gateway_arn  = aws_apigatewayv2_api.http_api.execution_arn
  route_key        = "PUT /prompt"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}


module "api_post_new_ai_response" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage       = var.stage

  lambda_name     = "api_post_new_ai_response"
  lambda_handler  = "api.ai.api_post_new_ai_response.api_post_new_ai_response.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/ai/api_post_new_ai_response/build.zip"

  lambda_layers = [
    aws_lambda_layer_version.layer_library_common_version.arn,
    aws_lambda_layer_version.layer_common_version.arn,
  ]

  environment_variables = {
    PROJECT_NAME = var.projectName
    STAGE_NAME   = var.stage
    OPEN_AI_KEY = var.openAIKey
  }

  api_gateway_id   = aws_apigatewayv2_api.http_api.id
  api_gateway_arn  = aws_apigatewayv2_api.http_api.execution_arn
  route_key        = "POST /ai"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}

module "api_post_new_ai_response_v2" {
  source = "../modules/api_endpoint"

  projectName = var.projectName
  stage       = var.stage

  lambda_name     = "api_post_new_ai_response_v2"
  lambda_handler  = "api.ai.api_post_new_ai_response_v2.api_post_new_ai_response_v2.lambda_handler"
  lambda_role_arn = aws_iam_role.default_iam_role.arn

  lambda_zip_path = "api/ai/api_post_new_ai_response_v2/build.zip"

  lambda_layers = [
    aws_lambda_layer_version.layer_library_common_version.arn,
    aws_lambda_layer_version.layer_common_version.arn,
  ]

  environment_variables = {
    PROJECT_NAME = var.projectName
    STAGE_NAME   = var.stage
    OPEN_AI_KEY = var.openAIKey
  }

  api_gateway_id   = aws_apigatewayv2_api.http_api.id
  api_gateway_arn  = aws_apigatewayv2_api.http_api.execution_arn
  route_key        = "POST /ai/v2"
  s3_source_bucket = aws_s3_bucket.source_build_bucket
}