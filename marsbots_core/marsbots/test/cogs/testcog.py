from discord.ext import commands

from marsbots_core.programs.ifttt import ifttt_get
from marsbots_core.programs.ifttt import ifttt_post
from marsbots_core.resources import modifiers


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

    def get_with_prob_message(self, name):
        return f"Hello from {name}, with probability 0.8"


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
