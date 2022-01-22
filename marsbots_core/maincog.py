from discord.ext import commands

from marsbots_core import config
from marsbots_core.resources.language_models import ExafunctionGPTJLanguageModel


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @commands.command()
    async def whereami(self, ctx: commands.context) -> None:
        await ctx.send(ctx.guild.id)

    @commands.command()
    async def complete(
        self,
        ctx: commands.context,
        max_tokens: int,
        *input_text: str,
    ) -> None:
        prompt = " ".join(input_text)
        lm = ExafunctionGPTJLanguageModel(api_key=config.LM_EXAFUNCTION_API_KEY)
        async with ctx.channel.typing():
            completion = lm.completion_handler(prompt, max_tokens=max_tokens)
            await ctx.send(prompt + completion)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
