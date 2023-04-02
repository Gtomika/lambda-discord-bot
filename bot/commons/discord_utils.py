ACK_TYPE = 1
DEFER_TYPE = 5


def is_from_guild(event) -> bool:
    return 'member' in event


def extract_username(event) -> str:
    if is_from_guild(event):
        return event['member']['user']['username']
    else:
        return event['user']['username']
