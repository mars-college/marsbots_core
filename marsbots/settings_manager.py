import json
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Union

from marsbots.util import pythonify_json


class SettingsManager(ABC):
    def __init__(self, settings: dict, defaults) -> None:
        self.settings = settings
        self.defaults = defaults

    @property
    @abstractmethod
    def is_initialized(self):
        raise NotImplementedError()

    @abstractmethod
    def initialize(self):
        raise NotImplementedError()

    @abstractmethod
    def load_settings(self):
        raise NotImplementedError()

    @abstractmethod
    def update_settings(self, updates):
        raise NotImplementedError()

    def initialize_guild(self, guild_id):
        self.settings[guild_id] = {}
        guild_settings = self.settings[guild_id]
        print("###########")
        print(self.defaults)
        for k, v in self.defaults.__dict__.items():
            guild_settings[k] = {}
            guild_settings[k]["default"] = v
            guild_settings[k]["channels"] = {}
        self.update_settings()
        return guild_settings

    def get_guild_settings(self, guild_id):
        guild_settings = self.settings.get(guild_id)
        if not guild_settings:
            guild_settings = self.initialize_guild(guild_id)
        return guild_settings

    def get_setting(self, guild_id, setting_name):
        guild_settings = self.get_guild_settings(guild_id)
        return guild_settings[setting_name]["default"]

    def get_channel_setting(self, channel_id, guild_id, setting_name):
        guild_settings = self.get_guild_settings(guild_id)
        setting = guild_settings[setting_name]
        channel_setting = setting["channels"].get(channel_id)
        return channel_setting if channel_setting else setting["default"]

    def update_setting(self, guild_id, setting_name, value):
        guild_settings = self.get_guild_settings(guild_id)
        guild_settings[setting_name]["default"] = value
        self.update_settings()

    def update_channel_setting(self, channel_id, guild_id, setting_name, value):
        guild_settings = self.get_guild_settings(guild_id)
        guild_settings[setting_name]["channels"][channel_id] = value
        self.update_settings()


class LocalSettingsManager(SettingsManager):
    def __init__(self, filepath: Union[Path, str], defaults) -> None:
        self.filepath = Path(filepath)
        self.settings = self.load_settings()
        super().__init__(self.settings, defaults)

    @property
    def is_initialized(self):
        if self.filepath.exists():
            return True
        return False

    def initialize(self):
        self.filepath.write_text(json.dumps({}))

    def load_settings(self):
        if not self.is_initialized:
            self.initialize()
        return pythonify_json(json.loads(self.filepath.read_text()))

    def update_settings(self):
        with open(self.filepath, "w") as f:
            json.dump(self.settings, f)


class MongoSettingsManager(SettingsManager):
    pass
