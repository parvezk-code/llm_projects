# services/llm/llm_service.py

from openai import OpenAI


class LLMService:

    def __init__(self, api_key: str, model: str):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def call(
        self,
        pdf_text: str,
        history: list[dict],
        user_message: str
    ) -> str:

        system_prompt = (
            "You are a helpful assistant. "
            "Answer questions based on the following PDF document:\n\n"
            f"{pdf_text}"
        )

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        return response.choices[0].message.content