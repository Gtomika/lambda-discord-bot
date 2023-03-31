import os
import datetime

from bot.commons import discord_interaction_responder as responder

aws_region = os.getenv('AWS_REGION')
function_name = os.getenv('AWS_LAMBDA_FUNCTION_NAME')
execution_environment = os.getenv('AWS_EXECUTION_ENV')


# This lambda is invoked by the discord interaction lambda
# event: Discord API interaction event
def lambda_handler(event, context):
    interaction_token = event['token']
    current_time = datetime.datetime.now()

    message = f"""
    The lambda function that responded to this command is {function_name}.
     - AWS Region: {aws_region}
     - Execution environment: {execution_environment}
    This lambda was executed at {current_time}
    """

    success = responder.respond_to_discord_interaction(interaction_token, message)
    if not success:
        print('Failed to send response to Lambda Info discord interaction')
