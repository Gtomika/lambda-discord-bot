import unittest.mock
import os
import json

mock_info_interaction = """
{
    "type": 2,
    "token": "cooltoken",
    "member": {
        "user": {
            "id": "53908232506183680",
            "username": "Mason",
            "avatar": "a_d5efa99b3eeaa7dd43acca82f5692432",
            "discriminator": "1337",
            "public_flags": 131141
        },
        "roles": ["539082325061836999"],
        "premium_since": null,
        "permissions": "2147483647",
        "pending": false,
        "nick": null,
        "mute": false,
        "joined_at": "2017-03-13T19:19:14.040000+00:00",
        "is_pending": false,
        "deaf": false
    },
    "id": "786008729715212338",
    "guild_id": "290926798626357999",
    "app_permissions": "442368",
    "guild_locale": "en-US",
    "locale": "en-US",
    "data": {
        "options": [],
        "type": 1,
        "name": "lambda_info",
        "id": "771825006014889984"
    },
    "channel_id": "645027906669510667"
}
"""


class TestInfoLambda(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['AWS_REGION'] = 'eu-central-1'
        os.environ['AWS_LAMBDA_FUNCTION_NAME'] = 'InfoCommandHandler'
        os.environ['AWS_EXECUTION_ENV'] = 'python3.9'

    @unittest.mock.patch(
        'bot.commons.discord_interaction_responder.respond_to_discord_interaction')
    def test_lambda_handler(self, mock_responder_method):
        # importing here simulates AWS lambda loading this file
        from ...info_lambda_function.info_lambda_function import lambda_handler
        lambda_handler(json.loads(mock_info_interaction), {})

        call_args = mock_responder_method.call_args
        self.assertTrue(call_args is not None)

        arguments = call_args[0]
        token = arguments[0]
        message: str = arguments[1]

        self.assertEqual('cooltoken', token)
        self.assertTrue('eu-central-1' in message)
        self.assertTrue('InfoCommandHandler' in message)
        self.assertTrue('python3.9' in message)


if __name__ == '__main__':
    unittest.main()

