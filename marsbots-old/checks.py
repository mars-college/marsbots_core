from typing import List

from discord.ext import commands


def only_allowed_in_guilds(
    guild_ids: List[int],
    error_message: str = "This command is not allowed in this server.",
):
    async def predicate(ctx):
        if ctx.guild.id not in guild_ids:
            raise commands.CheckFailure(error_message)
        return True

    return commands.check(predicate)


def only_allowed_in_channels(
    channel_ids: List[int],
    error_message: str = "This command is not allowed in this channel.",
):
    async def predicate(ctx):
        if ctx.channel.id not in channel_ids:
            raise commands.CheckFailure(error_message)
        return True

    return commands.check(predicate)


def not_allowed_in_dm(error_message: str = "This command is not allowed in DMs."):
    async def predicate(ctx):
        if not ctx.guild:
            raise commands.CheckFailure(error_message)
        return True

    return commands.check(predicate)
