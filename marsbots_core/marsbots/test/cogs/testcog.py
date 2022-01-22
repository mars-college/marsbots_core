from discord.ext import commands

from marsbots_core.programs import hey


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command()
    async def whereami(self, ctx: commands.context) -> None:
        await ctx.send("Hello from a custom cog")
        await ctx.send(ctx.guild.id)

    @commands.command()
    async def hey(self, ctx: commands.context) -> None:
        await ctx.send(hey())


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
