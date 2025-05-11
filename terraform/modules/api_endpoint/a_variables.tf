variable "projectName" {}
variable "stage" {}
variable "lambda_zip_path" {
  description = "Path to the local Lambda zip . src/{variable}"
  type        = string
  default = "layer/layer_library_common/layer.zip"
}
variable "lambda_name" {}
variable "lambda_handler" {}
variable "lambda_role_arn" {}
variable "environment_variables" {
  type    = map(string)
  default = {}
}
variable "lambda_layers" {
    type = list(string)
    default = []
}

variable "api_gateway_id" {}
variable "api_gateway_arn" {}
variable "route_key" {}  # e.g., "GET /users"
variable "s3_source_bucket" {}

