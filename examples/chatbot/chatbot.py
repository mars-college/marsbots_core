import discord
from discord.ext import commands

from . import prompts
from marsbots import config
from marsbots.models import ChatMessage
from marsbots.programs.lm import complete_text
from marsbots.resources.discord_utils import get_discord_messages
from marsbots.resources.discord_utils import get_reply_chain
from marsbots.resources.discord_utils import is_mentioned
from marsbots.resources.discord_utils import replace_bot_mention
from marsbots.resources.discord_utils import replace_mentions_with_usernames
from marsbots.resources.language_models import OpenAIGPT3LanguageModel


class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.language_model = OpenAIGPT3LanguageModel(config.LM_OPENAI_API_KEY)

        self.name = "Chatbot"
        self.should_follow_reply_chain = True

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if is_mentioned(message, self.bot.user):
            ctx = await self.bot.get_context(message)
            async with ctx.channel.typing():
                prompt = await self.format_prompt(ctx, message)
                completion = await complete_text(
                    self.language_model,
                    prompt,
                    max_tokens=80,
                    stop=["**[", "\n\n"],
                )
                await message.reply(completion)

    async def format_prompt(
        self,
        ctx: commands.context,
        message: discord.Message,
    ) -> str:
        last_messages = await get_discord_messages(ctx.channel, 1)
        reply_chain = await get_reply_chain(ctx, message, depth=6)
        if reply_chain:
            reply_chain = self.format_reply_chain(reply_chain)
        last_message_text = str(
            ChatMessage(
                f"{self.message_preprocessor(last_messages[0])}",
                message.author.display_name,
            ),
        ).strip()
        prompt = prompts.PREFIX

        if reply_chain and self.should_follow_reply_chain:
            prompt += f"{reply_chain}\n"

        prompt += "\n".join(
            [
                last_message_text,
                f"**[{self.name}]**:",
            ],
        )

        print(prompt)

        return prompt

    def format_reply_chain(self, messages):
        reply_chain = []
        for message in messages:
            if message.author.id == self.bot.user.id:
                sender_name = self.name
            else:
                sender_name = message.author.display_name
            reply_chain.append(
                ChatMessage(
                    content=f"{self.message_preprocessor(message)}",
                    sender=sender_name,
                ),
            )
        return "\n".join([str(message).strip() for message in reply_chain])

    def message_preprocessor(self, message: discord.Message) -> str:
        message_content = replace_bot_mention(message.content, only_first=True)
        message_content = replace_mentions_with_usernames(
            message_content,
            message.mentions,
        )
        message_content = message_content.strip()
        return message_content


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ExampleCog(bot))
