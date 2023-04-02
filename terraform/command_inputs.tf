# Here are declared all the IAM policies for the command lambda functions
# these ones do not require anything special, just logging

data "aws_iam_policy_document" "lambda_info_command_policy" {
  statement {
    sid = "AllowLambdaToLog"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

data "aws_iam_policy_document" "architecture_command_policy" {
  statement {
    sid = "AllowLambdaToLog"
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }
}

locals {
  # Here are declared the environmental variable configurations for the command lambda functions
  lambda_info_command_variables = {
    APPLICATION_ID = var.discord_application_id
    BOT_TOKEN = var.discord_bot_token
  }

  architecture_command_variables = {
    APPLICATION_ID = var.discord_application_id
    BOT_TOKEN = var.discord_bot_token
  }

  # Build map objects from the command inputs: to be used later
  command_policies = tomap({
    LambdaInfo = data.aws_iam_policy_document.lambda_info_command_policy
    ArchitectureChoice = data.aws_iam_policy_document.architecture_command_policy
  })

  environment_variables = tomap({
    LambdaInfo = local.lambda_info_command_variables
    ArchitectureChoice = local.architecture_command_variables
  })
}