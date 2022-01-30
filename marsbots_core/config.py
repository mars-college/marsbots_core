import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ENV = "DEV"

LM_OPENAI_API_KEY = os.getenv("LM_OPENAI_API_KEY")
LM_EXAFUNCTION_API_KEY = os.getenv("LM_EXAFUNCTION_API_KEY")
LM_AI21_API_KEY = os.getenv("LM_AI21_API_KEY")
LM_COHERE_API_KEY = os.getenv("LM_COHERE_API_KEY")

IFTTT_KEY = os.getenv("IFTTT_KEY")

CRASH_WEBHOOK_URL = os.getenv("CRASH_WEBHOOK_URL")
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID")) if os.getenv("TEST_GUILD_ID") else None
TEST_CHANNEL_ID = (
    int(os.getenv("TEST_CHANNEL_ID")) if os.getenv("TEST_CHANNEL_ID") else None
)
