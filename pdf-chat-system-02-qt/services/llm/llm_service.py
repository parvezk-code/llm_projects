# services/llm/llm_service.py

from openai import OpenAI


class LLMService:

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self._client      = OpenAI(api_key=api_key)
        self._model       = model
        self._temperature = temperature
        self._max_tokens  = max_tokens

    def call(self, messages: list[dict]) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        return response.choices[0].message.content