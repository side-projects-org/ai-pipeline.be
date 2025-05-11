resource "aws_apigatewayv2_api" "http_api" {
  name          = "${var.projectName}-${var.stage}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true

  depends_on = [module.api_get_sample_model_by_key.route_id]
}
