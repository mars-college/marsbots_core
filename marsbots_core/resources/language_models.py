from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

import cohere
import openai
import requests

from marsbots_core import config


class LanguageModel(ABC):
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    @abstractmethod
    def completion_handler(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


@dataclass
class OpenAIGPT3LanguageModelSettings:
    engine: str = "davinci"
    temperature: float = 1.0
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class OpenAIGPT3LanguageModel(LanguageModel):
    def __init__(
        self,
        model_name: str = "openai-gpt3",
        api_key: str = config.LM_OPENAI_API_KEY,
        **kwargs,
    ) -> None:
        self.settings = OpenAIGPT3LanguageModelSettings(**kwargs)
        openai.api_key = api_key
        super().__init__(model_name)

    def completion_handler(
        self,
        prompt: str,
        max_tokens: int,
        stop: list = None,
        **kwargs: any,
    ) -> str:
        print(kwargs)
        completion = openai.Completion.create(
            engine=self.settings.engine,
            prompt=prompt,
            max_tokens=max_tokens,
            stop=stop,
            temperature=kwargs.get("temperature") or self.settings.temperature,
            top_p=kwargs.get("top_p") or self.settings.top_p,
            frequency_penalty=kwargs.get("frequency_penalty")
            or self.settings.frequency_penalty,
            presence_penalty=kwargs.get("presence_penalty")
            or self.settings.presence_penalty,
        )
        completion_text = completion.choices[0].text
        return completion_text


@dataclass
class AI21JurassicLanguageModelSettings:
    model_type: str = "j1-jumbo"
    temperature: float = 1.0
    top_p: float = 1.0


class AI21JurassicLanguageModel(LanguageModel):
    def __init__(
        self,
        model_name: str = "ai21-jurassic",
        api_key: str = config.LM_AI21_API_KEY,
        **kwargs,
    ) -> None:
        self.settings = AI21JurassicLanguageModelSettings(**kwargs)
        self.api_key = api_key
        super().__init__(model_name)

    @property
    def api_url(self) -> str:
        return f"https://api.ai21.com/studio/v1/{self.settings.model_type}/complete"

    def completion_handler(
        self,
        prompt: str,
        max_tokens: int,
        stop: list = None,
        **kwargs: any,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "maxTokens": max_tokens,
            "temperature": kwargs.get("temperature") or self.settings.temperature,
            "topP": kwargs.get("top_p") or self.settings.top_p,
            "stopSequences": stop if stop else [],
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        completion = response.json()
        completion_text = completion["completions"][0]["data"]["text"]
        return completion_text


@dataclass
class CohereLanguageModelSettings:
    model_type: str = "large"
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: float = 0


class CohereLanguageModel(LanguageModel):
    def __init__(
        self,
        model_name: str = "cohere",
        api_key: str = config.LM_COHERE_API_KEY,
        **kwargs,
    ):
        self.client = cohere.Client(api_key)
        self.settings = CohereLanguageModelSettings(**kwargs)
        super().__init__(model_name)

    def completion_handler(self, prompt: str, max_tokens: int, **kwargs: any) -> str:
        prediction = self.client.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            model=kwargs.get("model_type") or self.settings.model_type,
            temperature=kwargs.get("temperature") or self.settings.model_type,
            k=kwargs.get("top_k") or self.settings.top_k,
            p=kwargs.get("top_p") or self.settings.top_p,
        )
        completion = prediction.generations[0].text
        return completion
