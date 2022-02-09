import discord
from discord.ext import commands

from marsbots_core import config
from marsbots_core.resources.discord_utils import is_mentioned
from marsbots_core.resources.language_models import OpenAIGPT3LanguageModel


class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.language_model = OpenAIGPT3LanguageModel(config.LM_OPENAI_API_KEY)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if is_mentioned(message, self.bot.user):
            await self.bot.get_context(message)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ExampleCog(bot))
