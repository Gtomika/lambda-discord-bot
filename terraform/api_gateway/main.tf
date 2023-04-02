locals {
  api_gateway_name = "API-${var.app_name}-${var.environment}-${var.aws_region}"
}

# Configure access logging for the API gateway
resource "aws_cloudwatch_log_group" "api_gateway_log_group" {
  name = "/aws/apigateway/${local.api_gateway_name}"
  retention_in_days = var.log_retention_days
}

# Configure the API gateway
resource "aws_apigatewayv2_api" "api_gateway" {
  name          = local.api_gateway_name
  protocol_type = "HTTP"
  description = "API Gateway for ${var.app_name} application, forwarding request to the discord interaction lambda"
}

resource "aws_apigatewayv2_route" "discord_interaction_route" {
  api_id    = aws_apigatewayv2_api.api_gateway.id
  route_key = "POST /${var.discord_interaction_path}"
}

resource "aws_apigatewayv2_integration" "discord_interaction_integration" {
  api_id           = aws_apigatewayv2_api.api_gateway.id
  integration_type = "AWS_PROXY"

  integration_method        = "POST"
  integration_uri           = var.discord_interaction_lambda_invocation_arn
  connection_type           = "INTERNET"
  content_handling_strategy = "CONVERT_TO_TEXT"
}

# API gateway stage and deployment

resource "aws_apigatewayv2_stage" "api_gateway_stage" {
  name          = var.environment
  api_id        = aws_apigatewayv2_api.api_gateway.id
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_log_group.arn
    format          = "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] $context.httpMethod $context.resourcePath $context.protocol $context.status $context.responseLength $context.requestId $context.extendedRequestId"
  }
}

resource "aws_apigatewayv2_deployment" "api_gateway_deployment" {
  name          = "Deploy-${local.api_gateway_name}"
  protocol_type = "HTTP"
  api_id        = aws_apigatewayv2_api.api_gateway.id

  # To avoid attempting deployment before route + integration are ready
  depends_on = [aws_apigatewayv2_integration.discord_interaction_integration, aws_apigatewayv2_route.discord_interaction_route]

  lifecycle { # to avoid downtime
    create_before_destroy = true
  }

  triggers = { # to avoid unnecessary re-deployments
    redeployment = sha1(join(",", tolist([
      jsonencode(aws_apigatewayv2_integration.discord_interaction_integration),
      jsonencode(aws_apigatewayv2_route.discord_interaction_route),
    ])))
  }
}

# Give permissions to API gateway to invoke interaction lambda
resource "aws_lambda_permission" "api_gateway_lambda_permission" {
  statement_id = "AllowAPIGatewayToInvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = var.discord_interaction_lambda_name
  principal     = "apigateway.amazonaws.com"
  # only allow this invocation from the exact path
  source_arn = "${aws_apigatewayv2_stage.api_gateway_stage.execution_arn}/${var.discord_interaction_path}"
}
