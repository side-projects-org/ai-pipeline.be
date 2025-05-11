resource "aws_s3_bucket" "source_build_bucket" {
    bucket = "${var.projectName}-${var.stage}-build"

    tags = {
        Name = "${var.projectName} ${var.stage} build bucket"
        Environment = var.stage
    }
}