# services/llm/llm_service.py

from openai import OpenAI


class LLMService:

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self._client      = OpenAI(api_key=api_key)
        self._model       = model
        self._temperature = temperature
        self._max_tokens  = max_tokens

    # call llm with messages without list of mcp tools
    def call(self, messages: list[dict]) -> str:
        response = self._client.chat.completions.create( model=self._model, messages=messages)
        return response.choices[0].message.content

    # call llm with messages with list of mcp tools
    def call_with_tool_list( self, messages: list[dict], tools: list[dict]) -> dict:
        
        response = self._client.chat.completions.create(
                            model=self._model,
                            messages=messages,
                            tools=tools,
                            tool_choice="auto"
        )
        # call_with_tool_list() returns full message dict
        # return response.choices[0].message.model_dump()
        
        return response.choices[0].message.model_dump()