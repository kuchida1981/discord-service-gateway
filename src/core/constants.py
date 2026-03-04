"""Discord API constants."""

from enum import IntEnum


class InteractionType(IntEnum):
    """Discord Interaction Type values."""

    PING = 1
    APPLICATION_COMMAND = 2


class InteractionResponseType(IntEnum):
    """Discord Interaction Response Type values."""

    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
