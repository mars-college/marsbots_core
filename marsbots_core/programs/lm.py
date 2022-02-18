import asyncio
from functools import partial

from charset_normalizer import logging

from marsbots_core.resources.language_models import LanguageModel
from marsbots_core.resources.language_models import OpenAIGPT3LanguageModel


async def complete_text(
    language_model: LanguageModel,
    prompt: str,
    max_tokens: int,
    use_content_filter: bool = False,
    **kwargs: any,
) -> str:
    logging.info(f"Completing text with prompt: {prompt}")
    loop = asyncio.get_running_loop()
    response_safe, max_tries, num_tries = False, 3, 0
    while num_tries < max_tries and not response_safe:
        completion_text = await loop.run_in_executor(
            None,
            partial(
                language_model.completion_handler,
                prompt=prompt,
                max_tokens=int(max_tokens),
                **kwargs,
            ),
        )
        num_tries += 1
        if (
            OpenAIGPT3LanguageModel.content_safe(completion_text)
            or not use_content_filter
        ):
            response_safe = True
        else:
            print(f"Completion flagged unsafe: {completion_text}")
            logging.info(f"Completion flagged unsafe: {completion_text}")
    if not response_safe:
        completion_text = "Sorry, try talking about something else."
    logging.info(f"Completed text: {completion_text}")
    return completion_text
