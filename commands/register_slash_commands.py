import requests
import os

create_command_url = 'https://discord.com/api/v10/applications/{application_id}/guilds/{guild_id}/commands'
application_id = os.getenv('APPLICATION_ID')
guild_id = os.getenv('GUILD_ID')
bot_token = os.getenv('BOT_TOKEN')


def register_slash_command(command_json_path: str):
    with open(command_json_path, 'r') as command_file:
        command_data = command_file.read()

    formatted_url = create_command_url.format(application_id=application_id, guild_id=guild_id)
    response = requests.post(formatted_url, data=command_data, headers={
        'Authorization': f'Bot {bot_token}',
        'Content-Type': 'application/json'
    })

    if response.status_code < 400:
        print(f'Registered discord slash command: {command_json_path}')
    else:
        print(f'{response.status_code} Error while registering slash command: {response.content}')


command_data_folder = os.path.join(os.path.dirname(__file__), 'commands_data')
print(f'Proceeding to register slash commands in {command_data_folder}')

command_data_files = os.listdir(command_data_folder)
for command_data_file in command_data_files:
    register_slash_command(os.path.join(os.path.dirname(__file__), 'commands_data', command_data_file))

print('Registered all slash commands')
