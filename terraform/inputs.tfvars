app_name = "LambdaDiscordBot"

commons_layer_deployment_path = "../common-layer-deployment-package/common_layer.zip"

discord_interaction_lambda_data = {
  handler = "bot/discord_interaction_lambda_function/lambda_function.lambda_handler"
  path_to_deployment_package = "../discord-interaction-lambda-package/discord_interaction_lambda.zip"
}

command_data = [
  {
    command_name = "LambdaInfo"
    command_name_discord = "lambda_info"
    handler = "bot/info_lambda_function/.lambda_handler"
    path_to_deployment_package = "../info-lambda-package/info_lambda.zip"
  },
  {
    command_name = "ArchitectureChoice"
    command_name_discord = "architecture_choice"
    handler = "bot/architecture_lambda_function/architecture_lambda_function.lambda_handler"
    path_to_deployment_package = "../architecture-lambda-package/architecture_lambda.zip"
  }
]

discord_application_id = 1089878825535549533
discord_application_public_key = "aa66cd8542274a1ae6ed42d4214ab7f7dfc5d85fc4fc50e1596119860222dc81"
discord_interaction_path = "api/discord/interaction"

log_retention_days = 30