from dataclasses import dataclass


@dataclass
class MarsBotSettings:
    name: str
    token_env: str
    command_prefix: str
