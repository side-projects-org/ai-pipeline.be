resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.projectName}-${var.stage}"
  protocol_type = "HTTP"

  cors_configuration {
    allow_credentials = null
    allow_headers     = ["*"]
#    allow_headers     = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent",]
    allow_methods     = ["*"]
    allow_origins     = ["http://localhost:3000", "http://localhost:3001", "https://main.d2x72b47hczm52.amplifyapp.com"]
    expose_headers    = null
    max_age           = 86400
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true

  depends_on = [module.api_get_sample_model_by_key.route_id]
}
