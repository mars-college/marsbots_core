import discord
from discord.commands import slash_command
from discord.ext import commands

from marsbots_core import config
from marsbots_core.models import ChatMessage
from marsbots_core.programs.ifttt import ifttt_get
from marsbots_core.programs.ifttt import ifttt_post
from marsbots_core.programs.lm import complete_text
from marsbots_core.resources.discord_utils import get_discord_messages
from marsbots_core.resources.discord_utils import is_mentioned
from marsbots_core.resources.language_models import OpenAIGPT3LanguageModel
from marsbots_core.resources.modifiers import with_probabilities


class ButtonView(discord.ui.View):
    def __init__(self):
        # making None is important if you want the button work after restart!
        super().__init__(timeout=None)

    # custom_id is required and should be unique for <commands.Bot.add_view>
    # attribute emoji can be used to include emojis which can be default str emoji or str(<:emojiName:int(ID)>)
    # timeout can be used if there is a timeout on the button interaction. Default timeout is set to 180.
    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        custom_id="counter:firstButton",
        label="Button",
    )
    async def leftButton(self, button, interaction):
        await interaction.response.edit_message(content="button was pressed!")


class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.language_model = OpenAIGPT3LanguageModel(config.LM_OPENAI_API_KEY)

    @commands.command()
    async def get_commands(self, ctx) -> None:
        print([c.qualified_name for c in self.walk_commands()])

    @commands.command()
    async def whereami(self, ctx) -> None:
        await ctx.send("Hello from a custom cog")
        await ctx.send(ctx.guild.id)

    @slash_command(guild_ids=[config.TEST_GUILD_ID])
    async def howami(self, ctx) -> None:
        await ctx.respond("doing great")

    @commands.command()
    async def get_messages(self, ctx: commands.Context) -> None:
        messages = await get_discord_messages(ctx.channel, 10)
        for message in messages:
            msg = ChatMessage(
                content=message.content,
                sender=message.author.name,
            )
            print(msg)

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
            completion = complete_text(self.language_model, prompt, max_tokens)
            await ctx.send(prompt + completion)

    @slash_command(guild_ids=[config.TEST_GUILD_ID])
    async def complete_some_text(
        self,
        ctx,
        max_tokens: int,
        prompt: str,
    ) -> None:
        completion = await complete_text(self.language_model, prompt, max_tokens)
        print(prompt + completion)
        await ctx.respond(prompt + completion)

    @slash_command(
        guild_ids=[config.TEST_GUILD_ID],
        name="slash_command_name",
        description="command description!",
    )
    async def button(self, ctx):
        navigator = ButtonView()
        await ctx.respond("press the button.", view=navigator)

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message) -> None:
        if is_mentioned(message, self.bot.user):
            await message.channel.send("Hello from a custom cog, you were mentioned.")

        autoreply = self.should_autoreply(message, 0.0)
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
                    self.complete,
                    (
                        "Hey dude what's up I'm going to",
                        40,
                    ),
                ),
                probability,
            ),
        )
        return reply


def setup(bot: commands.Bot) -> None:
    bot.add_cog(ExampleCog(bot))
