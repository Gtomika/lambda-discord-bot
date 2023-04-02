from bot.commons import discord_interaction_responder as responder
from bot.commons import discord_utils


# This lambda is invoked by the discord interaction lambda
# event: Discord API interaction event
def lambda_handler(event, context):
    interaction_token = event['token']
    user_name = discord_utils.extract_username(event)
    print(f'The user "{user_name}" invoked the command "architecture_choice"')

    options = event['data']['options']
    if len(options) > 0:
        # there is only 1 option: the first one, this is the one we are interested in
        selection = options[0]['value']
        process_selection(selection, user_name, interaction_token)
    else:
        responder.respond_to_discord_interaction(interaction_token, 'Error: you did not select an option!')


def process_selection(selection: str, guild_member_name: str, interaction_token: str):
    if selection == 'serverless':
        responder.respond_to_discord_interaction(interaction_token, f'Congratulations {guild_member_name},'
                                                                    ' that is a great choice!')
    else:
        responder.respond_to_discord_interaction(interaction_token, f'That is a mistake, {guild_member_name}!')
