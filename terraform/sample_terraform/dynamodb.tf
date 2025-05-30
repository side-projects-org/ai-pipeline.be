resource "aws_dynamodb_table" "default_dynamodb_table_sample" {
  name         = "${var.projectName}_${var.stage}_sample"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  attribute {
    name = "gsi_partition_key"
    type = "S"
  }
  attribute {
    name = "gsi_sort_key"
    type = "S"
  }

  global_secondary_index {
    name            = "sample_global_index"
    hash_key        = "gsi_partition_key"
    range_key       = "gsi_sort_key"
    projection_type = "ALL"
  }
}

# 이거 필요?
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

  # GSI 정의
  attribute {
    name = "prompt_name"
    type = "S"
  }

  attribute {
    name = "version"
    type = "S"
  }

  attribute {
    name = "created_at"
    type = "S"
  }

  global_secondary_index {
    name            = "prompt_name-version-index"
    hash_key        = "prompt_name"
    range_key       = "version"
    projection_type = "ALL"
  }
  global_secondary_index {
    name            = "prompt_name-created_at-index"
    hash_key        = "prompt_name"
    range_key       = "created_at"
    projection_type = "ALL"
  }
  global_secondary_index {
    name            = "version-prompt_name-index"
    hash_key        = "version"
    range_key       = "prompt_name"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "prompt_dynamodb_table_v2" {
  name         = "${var.projectName}_${var.stage}_prompt_v2"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"
  range_key    = "sk"

  attribute {
    name = "pk"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  # GSI 정의
  attribute {
    name = "item_type__prompt_name"
    type = "S"
  }

  attribute {
    name = "version"
    type = "S"
  }

  attribute {
    name = "prompt_name"
    type = "S"
  }

  attribute {
    name = "item_type__created_at"
    type = "S"
  }

  global_secondary_index {
    name            = "version-item_type__prompt_name-index"
    hash_key        = "version"
    range_key       = "item_type__prompt_name"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "prompt_name-item_type__created_at-index"
    hash_key        = "prompt_name"
    range_key       = "item_type__created_at"
    projection_type = "ALL"
  }
}