import re
from datetime import datetime
from typing import Optional

import discord
from charset_normalizer import logging
from discord.ext import commands

from marsbots_core import constants


def is_mentioned(message: discord.Message, user: discord.User) -> bool:
    """
    Checks if a user is mentioned in a message.
    :param message: The message to check.
    :param user: The user to check.
    :return: True if the user is mentioned, False otherwise.
    """
    return user.id in [m.id for m in message.mentions]


async def process_mention_as_command(
    ctx: str,
    cog: commands.Cog,
    command_not_found_response: str = constants.COMMAND_NOT_FOUND_MESSAGE,
):
    try:
        split_message = ctx.message.content.split(" ")
        message_text, args = split_message[1], split_message[2:]
        cmd = getattr(cog, message_text)
        await cmd(ctx, *args)
    except Exception as e:
        logging.error(e)
        await ctx.message.channel.send(command_not_found_response)


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


def remove_mentions(message_text: str) -> str:
    """
    Removes all mentions from a message.
    :param message: The message to remove mentions from.
    :return: The message with all mentions removed.
    """
    return re.sub(r"<@!\d+>", "", message_text)
