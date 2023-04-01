import unittest.mock
import json

mock_architecture_interaction_from_guild = """
{
    "type": 2,
    "token": "A_UNIQUE_TOKEN",
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
        "options": [{
            "type": 3,
            "name": "architecture",
            "value": "traditional"
        }],
        "type": 1,
        "name": "architecture_choice",
        "id": "771825006014889984"
    },
    "channel_id": "645027906669510667"
}
"""

mock_architecture_interaction_from_user = """
{
    "type": 2,
    "token": "A_UNIQUE_TOKEN",
    "user": {
        "id": "53908232506183680",
        "username": "Mason",
        "avatar": "a_d5efa99b3eeaa7dd43acca82f5692432",
        "discriminator": "1337",
        "public_flags": 131141
    },
    "id": "786008729715212338",
    "guild_id": "290926798626357999",
    "app_permissions": "442368",
    "guild_locale": "en-US",
    "locale": "en-US",
    "data": {
        "options": [{
            "type": 3,
            "name": "architecture",
            "value": "serverless"
        }],
        "type": 1,
        "name": "architecture_choice",
        "id": "771825006014889984"
    },
    "channel_id": "645027906669510667"
}
"""


class TestArchitectureLambda(unittest.TestCase):

    @unittest.mock.patch(
        'bot.commons.discord_interaction_responder.respond_to_discord_interaction')
    def test_archi_lambda_invoked_from_guild_traditional_choice(self, mock_responder_method):
        # simulate AWS lambda loading script
        from ...architecture_lambda_function.architecture_lambda_function import lambda_handler
        lambda_handler(json.loads(mock_architecture_interaction_from_guild), {})

        call_args = mock_responder_method.call_args
        self.assertTrue(call_args is not None)

        arguments = call_args[0]
        token = arguments[0]
        message = arguments[1]

        self.assertEqual('A_UNIQUE_TOKEN', token)
        self.assertEqual('That is a mistake, Mason!', message)

    @unittest.mock.patch(
        'bot.commons.discord_interaction_responder.respond_to_discord_interaction')
    def test_archi_lambda_invoked_from_dm_serverless_choice(self, mock_responder_method):
        # simulate AWS lambda loading script
        from ...architecture_lambda_function.architecture_lambda_function import lambda_handler
        lambda_handler(json.loads(mock_architecture_interaction_from_user), {})

        call_args = mock_responder_method.call_args
        self.assertTrue(call_args is not None)

        arguments = call_args[0]
        token = arguments[0]
        message = arguments[1]

        self.assertEqual('A_UNIQUE_TOKEN', token)
        self.assertEqual('Congratulations Mason, that is a great choice!', message)


if __name__ == '__main__':
    unittest.main()


