from ..commons import discord_interaction_responder as responder


# This lambda is invoked by the discord interaction lambda
# event: Discord API interaction event
def lambda_handler(event, context):
    interaction_token = event['token']
    # guaranteed to be invoked from a guild, so this will be present
    guild_member_name = event['member']['nick']

    # what the user chose is in this array
    options = event['data']['options']
    if len(options) > 0:
        # 'architecture' is what is specified as option name for this slash command
        selection = options['architecture']['value']
        process_selection(selection, guild_member_name, interaction_token)
    else:
        responder.respond_to_discord_interaction(interaction_token, 'Error: you did not select an option!')


def process_selection(selection: str, guild_member_name: str, interaction_token: str):
    if selection == 'serverless':
        responder.respond_to_discord_interaction(interaction_token, f'Congratulations {guild_member_name},'
                                                                    ' that is a great choice!')
    else:
        responder.respond_to_discord_interaction(interaction_token, f'That is a mistake, {guild_member_name}!')
