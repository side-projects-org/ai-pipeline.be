resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.projectName}-${var.stage}"
  protocol_type = "HTTP"
  cors_configuration {
    allow_origins = ["https://main.d2x72b47hczm52.amplifyapp.com", "http://localhost:3000"]
    allow_methods = ["*"]
    allow_headers = ["Content-Type", "Authorization"]
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true

}
