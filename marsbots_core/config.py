import os

from dotenv import load_dotenv

from marsbots_core import constants

load_dotenv(constants.DOTENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ENV = "DEV"

LM_OPENAI_API_KEY = os.getenv("LM_OPENAI_API_KEY")
LM_EXAFUNCTION_API_KEY = os.getenv("LM_EXAFUNCTION_API_KEY")
LM_AI21_API_KEY = os.getenv("LM_AI21_API_KEY")
LM_COHERE_API_KEY = os.getenv("LM_COHERE_API_KEY")
