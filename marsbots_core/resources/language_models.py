from abc import ABC
from abc import abstractmethod
from typing import Any

import cohere
import openai
import requests


class LanguageModel(ABC):
    def __init__(self, model_name: str, settings: dict) -> None:
        self.model_name = model_name
        self.settings = settings

    @abstractmethod
    def completion_handler(self, prompt: str, **kwargs: Any) -> str:
        raise NotImplementedError


class OpenAIGPT3LanguageModel(LanguageModel):
    def __init__(self, model_name: str = "openai-gpt3") -> None:
        settings = {
            "temperature": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.5,
        }
        super().__init__(model_name, settings)

    def completion_handler(
        self,
        prompt: str,
        max_tokens: int,
        stop: list = None,
    ) -> str:
        completion = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=max_tokens,
            frequency_penalty=self.settings["frequency_penalty"],
            temperature=self.settings["temperature"],
            presence_penalty=self.settings["presence_penalty"],
            stop=stop,
        )
        completion_text = completion.choices[0].text
        return completion_text


class ExafunctionGPTJLanguageModel(LanguageModel):
    def __init__(self, api_key: str, model_name: str = "exafunction-gptj") -> None:
        settings = {"temperature": 1.0, "min_tokens": 0}
        self.api_url = "https://nlp-server.exafunction.com/text_completion"
        self.api_key = api_key
        super().__init__(model_name, settings)

    def completion_handler(self, prompt: str, max_tokens: int, **kwargs: any) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "max_length": max_tokens,
            "min_length": self.settings["min_tokens"],
            "temperature": self.settings["temperature"],
            "remove_input": "true",
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        completion = response.json()
        completion_text = completion["text"]
        return completion_text


class AI21JurassicLanguageModel(LanguageModel):
    def __init__(
        self,
        api_key: str,
        model_type: str = "j1-jumbo",
        model_name: str = "ai21-jurassic",
    ) -> None:
        settings = {
            "model_type": model_type,
            "temperature": 1.0,
            "top_p": 1.0,
            "max_tokens": 16,
        }
        self.api_key = api_key
        super().__init__(model_name, settings)

    @property
    def api_url(self) -> str:
        return f"https://api.ai21.com/studio/v1/{self.settings['model_type']}/complete"

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
            "temperature": self.settings["temperature"],
            "topP": self.settings["top_p"],
            "stopSequences": stop if stop else [],
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        completion = response.json()
        completion_text = completion["completions"][0]["data"]["text"]
        return completion_text


class CohereLanguageModel(LanguageModel):
    def __init__(
        self,
        api_key: str,
        model_type: str = "large",
        model_name: str = "cohere",
    ):
        settings = {
            "model_type": model_type,
            "temperature": 1.0,
            "top_k": 0,
            "top_p": 1.0,
            "max_tokens": 50,
        }
        self.api_key = api_key
        super().__init__(model_name, settings)

    def completion_handler(self, prompt: str, max_tokens: int, **kwargs: any) -> str:
        co = cohere.Client(self.api_key)
        prediction = co.generate(
            model=self.settings["model_type"],
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=self.settings["temperature"],
            k=self.settings["top_k"],
            p=self.settings["top_p"],
        )
        completion = prediction.generations[0].text
        return completion
