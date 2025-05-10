resource "aws_s3_bucket" "source_build_bucket" {
    bucket = "${var.projectName}-${var.stage}-build"

    tags = {
        Name = "${var.projectName} ${var.stage} build bucket"
        Environment = var.stage
    }
}

resource "aws_s3_object" "s3_for_layer_library_common" {
    # count = fileexists("../src/layer/layer_library_common/layer.zip") ? 1 : 0

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/layer/layer_library_common/layer.zip"
    source = "../src/layer/layer_library_common/layer.zip"

    source_hash = filesha256("../src/layer/layer_library_common/build.zip")

    depends_on = [aws_s3_bucket.source_build_bucket]
}



resource "aws_lambda_layer_version" "layer_library_common_version" {
    # count = fileexists("../src/layer/layer_library_common/layer.zip") ? 1 : 0

    layer_name = "${var.projectName}_layer_library_common"

    s3_bucket         = aws_s3_object.s3_for_layer_library_common.bucket
    s3_key            = aws_s3_object.s3_for_layer_library_common.key
    s3_object_version = aws_s3_object.s3_for_layer_library_common.version_id

    compatible_architectures = ["arm64"]
    compatible_runtimes = ["python3.12"]

    source_code_hash = filesha256("../src/layer/layer_library_common/layer.zip")

    depends_on = [aws_s3_object.s3_for_layer_library_common]
}

resource "aws_s3_object" "s3_for_layer_common" {
    # count = fileexists("../src/common/layer.zip") ? 1 : 0

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/common/layer.zip"
    source = "../src/common/layer.zip"

    source_hash = filesha256("../src/common/build.zip")

    depends_on = [aws_s3_bucket.source_build_bucket]
}

resource "aws_lambda_layer_version" "layer_common_version" {
    # count = fileexists("../src/common/layer.zip") ? 1 : 0

    layer_name = "${var.projectName}_layer_common"

    s3_bucket         = aws_s3_object.s3_for_layer_common.bucket
    s3_key            = aws_s3_object.s3_for_layer_common.key
    s3_object_version = aws_s3_object.s3_for_layer_common.version_id

    compatible_architectures = ["arm64"]
    compatible_runtimes = ["python3.12"]

    source_code_hash = filesha256("../src/common/layer.zip")

    depends_on = [aws_s3_object.s3_for_layer_common]
}

resource "aws_s3_object" "s3_for_lambda_api_sample_api_get_sample_model_by_key" {
    # count = fileexists("../src/api/sample/api_get_sample_model_by_key/layer.zip") ? 1 : 0

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/api/sample/api_get_sample_model_by_key"
    source = "../src/api/sample/api_get_sample_model_by_key/build.zip"

    source_hash = filesha256("../src/api/sample/api_get_sample_model_by_key/build.zip")

    depends_on = [aws_s3_bucket.source_build_bucket]
}

data "aws_iam_policy_document" "iam_for_lambda_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = [
        "lambda.amazonaws.com",
        "sqs.amazonaws.com",
        "rds.amazonaws.com",
        "dynamodb.amazonaws.com",
      ]
      type = "Service"
    }
    effect = "Allow"
  }
}

resource "aws_iam_role" "default_iam_role" {
    name = "${var.projectName}_default_iam_role"


    assume_role_policy = data.aws_iam_policy_document.iam_for_lambda_role.json
}

resource "aws_lambda_function" "lambda_for_api_sample_api_get_sample_model_by_key" {
    # count = fileexists("../src/layer/layer_library_common/build.zip") ? 1 : 0
    role = aws_iam_role.default_iam_role.arn

    function_name = "${var.projectName}_api_get_sample_model_by_key"

    s3_bucket         = aws_s3_object.s3_for_lambda_api_sample_api_get_sample_model_by_key.bucket
    s3_key            = aws_s3_object.s3_for_lambda_api_sample_api_get_sample_model_by_key.key
    s3_object_version = aws_s3_object.s3_for_lambda_api_sample_api_get_sample_model_by_key.version_id

    handler = "api.sample.api_get_sample_model_by_key.api_get_sample_model_by_key.lambda_handler"

    runtime     = "python3.12"
    architectures = ["arm64"]
    memory_size = 128
    timeout     = 60

    tags = {
        Name = "${var.projectName}_api_get_sample_model_by_key"
    }

    layers = [
        aws_lambda_layer_version.layer_library_common_version.arn,
        aws_lambda_layer_version.layer_common_version.arn,
    ]

    environment {
        variables = {
            project_name = var.projectName
            stage_name   = var.stage
        }
    }

    source_code_hash = filesha256("../src/api/sample/api_get_sample_model_by_key/build.zip")

    depends_on = [aws_s3_bucket.source_build_bucket]
}

