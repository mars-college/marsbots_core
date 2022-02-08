import logging
import re
from datetime import datetime
from typing import List
from typing import Optional

import discord
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


def replace_bot_mention(
    message_text: str,
    only_first: bool = True,
    replacement_str: str = "",
) -> str:
    """
    Removes all mentions from a message.
    :param message: The message to remove mentions from.
    :return: The message with all mentions removed.
    """
    if only_first:
        return re.sub(r"<@!\d+>", replacement_str, message_text, 1)
    else:
        return re.sub(r"<@!\d+>", replacement_str, message_text)


async def get_reply_chain(
    ctx,
    message: discord.Message,
    depth: int,
) -> List[discord.Message]:
    messages = []
    count = 0
    while message and message.reference and count < depth:
        message = await ctx.fetch_message(message.reference.message_id)
        messages.append(message)
        count += 1
    messages.reverse()
    return messages


def replace_mentions_with_usernames(message_content: str, mentions) -> str:
    """
    Replaces all mentions with their usernames.
    :param message_content: The message to replace mentions in.
    :return: The message with all mentions replaced with their usernames.
    """
    for mention in mentions:
        message_content = message_content.replace(f"<@!{mention.id}>", mention.name)
    return message_content


def in_channels(channel_ids: List[int]) -> commands.check:
    async def predicate(ctx):
        if ctx.channel.id in channel_ids:
            return True
        print("command not valid in channel")

    return commands.check(predicate)


async def wait_for_user_reply(bot: commands.Bot, sender_id: int) -> discord.Message:
    """
    Waits for a user to reply to a message.
    :return: The message the user replied to.
    """

    def check(message: discord.Message) -> bool:
        return sender_id == message.author.id

    return await bot.wait_for("message", check=check)
