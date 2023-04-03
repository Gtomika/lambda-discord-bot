import os
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import json
import boto3

from bot.commons import api_gateway_interactions as agi
from bot.commons.discord_utils import ACK_TYPE, DEFER_TYPE

# Request verification
application_public_key = os.getenv('APPLICATION_PUBLIC_KEY')
verify_key = VerifyKey(bytes.fromhex(application_public_key))
signature_header_name = 'X-Signature-Ed25519'
timestamp_header_name = 'X-Signature-Timestamp'

# JSON serialized data of commands
commands_data_json = os.getenv('COMMANDS')
commands_data = json.loads(commands_data_json)

lambda_client = boto3.client('lambda')


# this lambda handler receives interaction events from Discord,
# through the AWS API Gateway
def lambda_handler(event, context):
    headers, body = agi.parse_api_gateway_event(event)
    body_raw = json.dumps(body)

    # Required by Discord to perform check to validate that this call came from them
    if not is_request_verified(headers, body_raw):
        return agi.to_api_gateway_raw_response(401, 'invalid request signature')

    body = json.loads(body_raw)
    # ACK message that is required for Discord interaction URL
    if body['type'] == ACK_TYPE:
        return agi.to_api_gateway_response(200, {
            'type': ACK_TYPE
        })

    # trigger another lambda that will update response later (async)
    return trigger_slash_command_handler_lambda(body, body_raw)


def trigger_slash_command_handler_lambda(body, body_raw: str) -> str:
    received_command_name = body['data']['name']
    for command_data in commands_data:
        if received_command_name == command_data['command_name_discord']:
            lambda_client.invoke(  # async invokes the lambda
                FunctionName=command_data['command_lambda_arn'],
                InvocationType='Event',
                Payload=body_raw
            )
            return defer_response()
    # this command was not provided in 'COMMANDS' variable in Terraform
    return agi.to_api_gateway_raw_response(500, f'Slash command {received_command_name} not found and cannot be processed')


def defer_response():
    return agi.to_api_gateway_response(200, {
        'type': DEFER_TYPE
    })


def is_request_verified(headers, body_raw: str) -> bool:
    if signature_header_name in headers and timestamp_header_name in headers:
        signature = headers[signature_header_name]
        timestamp = headers[timestamp_header_name]
    else:
        print(f'Either {signature_header_name} or {timestamp_header_name} header '
              f'was not found in the request: both are required')
        return False

    try:
        verify_key.verify(f'{timestamp}{body_raw}'.encode(), bytes.fromhex(signature))
        return True
    except Exception as e:  # any exception results in false
        print(f'Exception while validating request: {str(e)}')
        return False
