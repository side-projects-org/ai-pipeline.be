data "aws_iam_policy_document" "iam_for_lambda_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      identifiers = [
        "lambda.amazonaws.com",
        "sqs.amazonaws.com",
        "rds.amazonaws.com"
      ]
      type = "Service"
    }
    effect = "Allow"
  }
}
data "aws_iam_policy_document" "iam_for_lambda_policy" {
  version = "2012-10-17"
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:GetLogEvents",
      "logs:FilterLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
    effect    = "Allow"
  }

  statement {
    actions = [
      "dynamodb:DescribeReservedCapacity*",
      "dynamodb:DescribeLimits",

      "dynamodb:ListContributorInsights",
      "dynamodb:ListExports",
      "dynamodb:ListGlobalTables",
      "dynamodb:ListTables",

      "dynamodb:ListStreams",
      "dynamodb:ListBackups"
    ]
    resources = ["*"]
    effect    = "Allow"
    sid       = "ListAndDescribeNoLimit"
  }

  statement {
    actions = [
      "dynamodb:BatchGet*",
      "dynamodb:Get*",

      "dynamodb:DescribeStream",
      "dynamodb:DescribeTable",
      "dynamodb:DescribeTimeToLive",
      "dynamodb:Query",
      "dynamodb:Scan"
    ]
    resources = [
      "arn:aws:dynamodb:${var.awsRegion}:*:table/*",
      "arn:aws:dynamodb:${var.awsRegion}:*:*/index/*"
    ]
    effect = "Allow"
    sid    = "ListAndDescribe"
  }

  statement {
    actions = [
      "dynamodb:BatchWrite*",
      "dynamodb:Delete*",
      "dynamodb:Update*",

      "dynamodb:PutItem"
    ]
    resources = [
      "arn:aws:dynamodb:${var.awsRegion}:*:table/*",
      "arn:aws:dynamodb:${var.awsRegion}:*:*/index/*"
    ]
    effect = "Allow"
    sid    = "SpecificTable"
  }

  statement {
    actions = [
      "tag:GetTagKeys",
      "tag:GetTagValues"
    ]
    resources = ["*"]
    effect    = "Allow"
  }

#  statement {
#    effect  = "Allow"
#    actions = [
#      "s3:GetBucket*",
#      "s3:GetObject*"
#    ]
#    resources = [
#      "arn:aws:s3:::secretkey-for-oauth",
#      "arn:aws:s3:::secretkey-for-oauth/*"
#    ]
#  }

  statement {
    effect  = "Allow"
    actions = [
      "sqs:GetQueueUrl",
      "sqs:SendMessage",
#      "sqs:ReceiveMessage",
#      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = ["arn:aws:sqs:*:*:*"]
  }

  statement {
    effect  = "Allow"
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes"
    ]
    resources = ["arn:aws:sqs:*:*:*"]
  }
}


resource "aws_iam_role" "default_iam_role" {
    name = "${var.projectName}_default_iam_role"

    assume_role_policy = data.aws_iam_policy_document.iam_for_lambda_role.json
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "default_iam_policy" {
  name        = "${var.projectName}_default_iam_policy"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = data.aws_iam_policy_document.iam_for_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "default_iam_role_policy_attachment" {
  role       = aws_iam_role.default_iam_role.name
  policy_arn = aws_iam_policy.default_iam_policy.arn
}
