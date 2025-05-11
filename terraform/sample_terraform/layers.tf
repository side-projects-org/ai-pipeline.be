
resource "aws_s3_object" "s3_for_layer_library_common" {
    # count = fileexists("../src/layer/layer_library_common/layer.zip") ? 1 : 0

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/layer/layer_library_common/layer.zip"
    source = "../../src/layer/layer_library_common/layer.zip"

    source_hash = filesha256("../../src/layer/layer_library_common/layer.zip")

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

    source_code_hash = filesha256("../../src/layer/layer_library_common/layer.zip")

    depends_on = [aws_s3_object.s3_for_layer_library_common]
}

resource "aws_s3_object" "s3_for_layer_common" {
    # count = fileexists("../src/common/layer.zip") ? 1 : 0

    bucket = "${var.projectName}-${var.stage}-build"
    key = "build/${var.projectName}/common/layer.zip"
    source = "../../src/common/layer.zip"

    source_hash = filesha256("../../src/common/layer.zip")

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

    source_code_hash = filesha256("../../src/common/layer.zip")

    depends_on = [aws_s3_object.s3_for_layer_common]
}