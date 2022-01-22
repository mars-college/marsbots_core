import argparse
import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from marsbots_core.models import MarsBotSettings

load_dotenv()


class MarsBot(commands.Bot):
    def __init__(self, specfile_path: str) -> None:
        intents = discord.Intents.all()
        self.settings = self.load_settings(specfile_path)
        commands.Bot.__init__(
            self,
            command_prefix=self.settings.command_prefix,
            intents=intents,
        )

    def load_settings(self, specfile_path: str) -> MarsBotSettings:
        settings = json.load(open(specfile_path))
        return MarsBotSettings(**settings)

    async def on_ready(self) -> None:
        print(f"Running {self.settings.name}...")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)


def start(specfile_path: str, cog_path: str) -> None:
    print("Launching bot...")
    bot = MarsBot(specfile_path)
    print(cog_path)
    if cog_path:
        bot.load_extension(cog_path)
    else:
        bot.load_extension("maincog")
    bot.run(os.getenv(bot.settings.token_env))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MarsBot")
    parser.add_argument("specfile", help="specfile path")
    parser.add_argument("--cog-path", help="Path to a custom cog file")
    args = parser.parse_args()
    start(args.specfile, args.cog_path)
