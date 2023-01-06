from dataclasses import dataclass
from typing import List


@dataclass
class MarsBotMetadata:
    name: str
    token_env: str
    command_prefix: str
    intents: List[str]


@dataclass
class MarsBotCommand:
    name: str
    is_listener: bool
    allowed_guilds: List[int]
    allowed_channels: List[int]
    allowed_in_dm: bool
    allowed_users: List[int]


@dataclass
class MarsBot:
    metadata: MarsBotMetadata
    commands: List[MarsBotCommand]


@dataclass
class ChatMessage:
    content: str
    sender: str
    deliniator_left: str = "**["
    deliniator_right: str = "]**:"

    def __str__(self) -> str:
        return (
            f"{self.deliniator_left}{self.sender}{self.deliniator_right} {self.content}"
        )
