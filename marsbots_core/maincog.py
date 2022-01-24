from discord.ext import commands


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command()
    async def whereami(self, ctx: commands.context) -> None:
        await ctx.send(ctx.guild.id)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
