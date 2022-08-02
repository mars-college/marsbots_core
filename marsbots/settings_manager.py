import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Union

from discord.ext import commands


class SettingsManager(ABC):
    def __init__(self, cog: commands.Cog) -> None:
        self.cog = cog

    @abstractmethod
    def create(self):
        """Create a new settings backend."""
        raise NotImplementedError()

    @abstractmethod
    def is_created(self):
        """Check if the settings backend is created."""
        raise NotImplementedError()

    @abstractmethod
    def initialize(self):
        """Initialize the settings backend. Run each time the bot starts."""
        raise NotImplementedError()


class LocalSettingsManager(SettingsManager):
    def __init__(self, filepath: Union[Path, str], cog: commands.Cog, defaults) -> None:
        self.filepath = Path(filepath)
        self.defaults = defaults
        super().__init__(cog)
        self.initialize()

    def create(self):
        self.filepath.write_text(
            json.dumps(
                {
                    "commands": {},
                    "settings": {},
                },
            ),
        )

    def is_created(self):
        return self.filepath.exists()

    def initialize(self):
        if not self.is_created():
            self.create()
        print(self.defaults)
        print([command.name for command in self.cog.get_commands()])
        print([listener[0] for listener in self.cog.get_listeners()])


class MongoSettingsManager(SettingsManager):
    pass
