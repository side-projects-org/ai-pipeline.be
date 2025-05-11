output "lambda_function_name" {
  value = aws_lambda_function.lambda.function_name
}

output "route_id" {
  value = aws_apigatewayv2_route.route.id
}