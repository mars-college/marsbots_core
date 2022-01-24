import argparse
import json
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from marsbots_core import constants
from marsbots_core.models import MarsBotSettings


class MarsBot(commands.Bot):
    def __init__(self, specfile_path: str) -> None:
        intents = discord.Intents.all()
        self.settings = self.load_settings(specfile_path)
        self.configure_logging()
        commands.Bot.__init__(
            self,
            command_prefix=self.settings.command_prefix,
            intents=intents,
        )

    def load_settings(self, specfile_path: str) -> MarsBotSettings:
        settings = json.load(open(specfile_path))
        return MarsBotSettings(**settings)

    def configure_logging(self) -> None:
        logdir = constants.LOG_DIR / self.settings.name
        logfile = str(logdir / "discord.log")
        logdir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%a, %d %b %Y %H:%M:%S",
            filename=logfile,
            filemode="w",
            force=True,
        )

    async def on_ready(self) -> None:
        print(f"Running {self.settings.name}...")
        logging.info(f"Running {self.settings.name}...")

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        await self.process_commands(message)


def start(
    specfile_path: str,
    cog_path: str,
    dotenv_path: str = constants.DOTENV_PATH,
) -> None:

    print("Launching bot...")
    logging.info("Launching bot...")
    load_dotenv(dotenv_path)

    bot = MarsBot(specfile_path)
    if cog_path:
        bot.load_extension(cog_path)
    else:
        bot.load_extension("maincog")
    bot.run(os.getenv(bot.settings.token_env))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MarsBot")
    parser.add_argument("specfile", help="specfile path")
    parser.add_argument("--cog-path", help="Path to a custom cog file")
    parser.add_argument("--dotenv-path", help="Path to a custom .env file")
    args = parser.parse_args()
    start(args.specfile, args.cog_path, args.dotenv_path)
