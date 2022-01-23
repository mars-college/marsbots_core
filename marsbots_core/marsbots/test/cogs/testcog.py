import asyncio
from functools import partial

import discord
from discord.ext import commands

from marsbots_core import config
from marsbots_core.programs.ifttt import ifttt_get
from marsbots_core.programs.ifttt import ifttt_post
from marsbots_core.resources.discord_utils import is_mentioned
from marsbots_core.resources.language_models import OpenAIGPT3LanguageModel
from marsbots_core.resources.modifiers import with_probabilities


class HelperCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.language_model = OpenAIGPT3LanguageModel(config.LM_OPENAI_API_KEY)

    @commands.command()
    async def whereami(self, ctx: commands.context) -> None:
        await ctx.send("Hello from a custom cog")
        await ctx.send(ctx.guild.id)

    @commands.command()
    async def maybe_hello(self, ctx: commands.context) -> None:
        msg = with_probabilities(
            ((self.get_with_prob_message, ("jmill",)), 0.4),
            ((self.get_with_prob_message, ("JMILL",)), 0.4),
        )
        if msg:
            func, args = msg
            await ctx.send(func(*args))
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

    @commands.command()
    async def complete(
        self,
        ctx: commands.context,
        max_tokens: int,
        *input_text: str,
    ) -> None:
        prompt = " ".join(input_text)
        async with ctx.channel.typing():
            completion = self.complete_text(prompt, max_tokens)
            await ctx.send(prompt + completion)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if is_mentioned(message, self.bot.user):
            await message.channel.send("Hello from a custom cog, you were mentioned.")

        autoreply = self.should_autoreply(message, 0.5)
        if autoreply:
            async with message.channel.typing():
                func, args = autoreply
                completion = await func(*args)
                prompt = args[0]
                await message.channel.send(prompt + completion)

    def get_with_prob_message(self, name):
        return f"Hello from {name}"

    def should_autoreply(self, message: discord.Message, probability: float) -> None:
        reply = with_probabilities(
            (
                (
                    self.complete_text,
                    (
                        "Hey dude what's up I'm going to",
                        40,
                    ),
                ),
                probability,
            ),
        )
        return reply

    async def complete_text(self, prompt, max_tokens):
        loop = asyncio.get_running_loop()
        max_tokens = int(max_tokens)
        completion_text = await loop.run_in_executor(
            None,
            partial(
                self.language_model.completion_handler,
                prompt=prompt,
                max_tokens=max_tokens,
            ),
        )
        return completion_text


def setup(bot: commands.Bot) -> None:
    bot.add_cog(HelperCog(bot))
