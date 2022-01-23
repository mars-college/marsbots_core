from datetime import datetime
from typing import Optional

import discord


def is_mentioned(message: discord.Message, user: discord.User) -> bool:
    """
    Checks if a user is mentioned in a message.
    :param message: The message to check.
    :param user: The user to check.
    :return: True if the user is mentioned, False otherwise.
    """
    return user.id in [m.id for m in message.mentions]


async def get_discord_messages(
    channel: discord.TextChannel,
    limit: int,
    time: Optional[datetime] = None,
) -> list:
    """
    Gets the last x messages from a channel.
    :param channel: The channel to get the messages from.
    :param limit: The number of messages to get.
    :return: The last x messages from the channel.
    """
    if time is None:
        time = datetime.utcnow()

    raw_messages = await channel.history(
        limit=limit,
        oldest_first=False,
        before=time,
    ).flatten()

    raw_messages.reverse()

    return raw_messages
