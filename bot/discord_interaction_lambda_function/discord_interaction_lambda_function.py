import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json
import boto3

from bot.commons import discord_interaction_responder as responder
from bot.commons import api_gateway_interactions as agi
from bot.commons.discord_constants import ACK_TYPE, DEFER_TYPE

application_public_key = os.getenv('APPLICATION_PUBLIC_KEY')
verify_key = VerifyKey(bytes.fromhex(application_public_key))

# JSON serialized data of commands
commands_data_json = os.getenv('COMMANDS')
'''
Expected format: list of command objects
[
    {
        "command_name_discord": "lambda_info",
        "command_lambda_arn": "arn:aws:..."
    },
    ...
]
'''
commands_data = json.loads(commands_data_json)

lambda_client = boto3.client('lambda')

# this lambda handler receives interaction events from Discord,
# through the AWS API Gateway
def lambda_handler(event, context):
    headers, body_raw = agi.parse_api_gateway_event(event)

    # Required by Discord to perform check to validate that this call came from them
    if not is_request_verified(headers, body_raw):
        return agi.to_api_gateway_response(401, {
            'error': 'Request is invalid'
        })

    body = json.loads(body_raw)
    # ACK message that is required for Discord interaction URL
    if body['type'] == ACK_TYPE:
        return agi.to_api_gateway_response(200, {
            'type': ACK_TYPE
        })

    # trigger another lambda that will update response later (async)
    return trigger_slash_command_handler_lambda(body, body_raw)


def trigger_slash_command_handler_lambda(body, bodyRaw: str):
    received_command_name = body['data']['name']
    for command_data in commands_data:
        if received_command_name == command_data['command_name_discord']:
            lambda_client.invoke(  # async invokes the lambda
                FunctionName=command_data['command_lambda_arn'],
                InvocationType='Event',
                Payload=bodyRaw
            )
            return defer_response()
    # this command was not provided in 'COMMANDS' variable in Terraform
    return agi.to_api_gateway_response(500, {
        'error': f'Slash command {received_command_name} not found and cannot be processed'
    })


def defer_response():
    return agi.to_api_gateway_response(200, {
        'type': DEFER_TYPE
    })


def is_request_verified(headers, body_raw: str) -> bool:
    signature = headers["X-Signature-Ed25519"]
    timestamp = headers["X-Signature-Timestamp"]

    try:
        verify_key.verify(f'{timestamp}{body_raw}'.encode(), bytes.fromhex(signature))
        return True
    except BadSignatureError:
        return False
