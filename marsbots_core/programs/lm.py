import asyncio
from functools import partial

from charset_normalizer import logging

from marsbots_core.resources.language_models import LanguageModel


async def complete_text(
    language_model: LanguageModel,
    prompt: str,
    max_tokens: int,
    stop: list = None,
) -> str:
    logging.info(f"Completing text with prompt: {prompt}")
    loop = asyncio.get_running_loop()
    max_tokens = int(max_tokens)
    completion_text = await loop.run_in_executor(
        None,
        partial(
            language_model.completion_handler,
            prompt=prompt,
            max_tokens=max_tokens,
            stop=stop,
        ),
    )
    logging.info(f"Completed text: {completion_text}")
    return completion_text
