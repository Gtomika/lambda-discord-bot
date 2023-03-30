output "discord_interaction_lambda_arn" {
  value = aws_lambda_function.discord_interaction_lambda.arn
}

output "discord_interaction_lambda_name" {
  value = aws_lambda_function.discord_interaction_lambda.function_name
}