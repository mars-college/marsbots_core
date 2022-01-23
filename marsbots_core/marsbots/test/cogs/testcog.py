import discord
from discord.ext import commands

from marsbots_core.programs.ifttt import ifttt_get
from marsbots_core.programs.ifttt import ifttt_post
from marsbots_core.resources import modifiers
from marsbots_core.resources.discord_utils import is_mentioned


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command()
    async def whereami(self, ctx: commands.context) -> None:
        await ctx.send("Hello from a custom cog")
        await ctx.send(ctx.guild.id)

    @commands.command()
    async def maybe_hello(self, ctx: commands.context) -> None:
        msg = modifiers.with_probabilities(
            ((self.get_with_prob_message, ("jmill",)), 0.4),
            ((self.get_with_prob_message, ("JMILL",)), 0.4),
        )
        if msg:
            await ctx.send(msg)
        else:
            await ctx.send("Hello from a custom cog, you lowrolled.")

    @commands.command()
    async def test_ifttt(self, ctx: commands.context) -> None:
        await ctx.send("testing ifttt")
        ifttt_get("test")

    @commands.command()
    async def test_ifttt_post(self, ctx: commands.context) -> None:
        await ctx.send("testing ifttt post")
        ifttt_post("test_post", {"value1": "hey"})

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        print(message.mentions)
        if is_mentioned(message, self.bot.user):
            await message.channel.send("Hello from a custom cog, you were mentioned.")

    def get_with_prob_message(self, name):
        return f"Hello from {name}"


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
