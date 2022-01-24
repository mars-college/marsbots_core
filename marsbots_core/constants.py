from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
DOTENV_PATH = ROOT_DIR / ".env"
LOG_DIR = ROOT_DIR / "logs"

COMMAND_NOT_FOUND_MESSAGE = "Command not found."
