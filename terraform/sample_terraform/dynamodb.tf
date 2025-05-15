
resource "aws_dynamodb_table" "default_dynamodb_table" {
  name         = "${var.projectName}-${var.stage}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "key"

  attribute {
    name = "key"
    type = "S"
  }
}


resource "aws_dynamodb_table" "prompt_dynamodb_table" {
  name         = "${var.projectName}_${var.stage}_prompt"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "key"

  attribute {
    name = "key"
    type = "S"
  }
}
