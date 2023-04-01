ACK_TYPE = 1
DEFER_TYPE = 5


def is_from_guild(event) -> bool:
    return 'member' in event
