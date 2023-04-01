import json


def parse_api_gateway_event(event):
    return event['headers'], event['body']


def to_api_gateway_response(status_code: int, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'isBase64Encoded': False,
        'body': json.dumps(body)
    }
