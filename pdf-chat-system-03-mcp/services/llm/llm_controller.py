# services/llm/llm_controller.py

from services.llm.llm_service  import LLMService
from services.llm.llm_request  import LLMRequest
from services.llm.llm_response import LLMResponse

# agentic loop from main controller
class LLMController:

    def __init__(self, llm_service: LLMService, available_tools: list[dict]):
        self._llm_service     = llm_service
        self._available_tools = available_tools

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def ask_with_tools(self, request: LLMRequest) -> LLMResponse:
        """Send current running_messages to the LLM and return a parsed LLMResponse.
        
        The main controller calls this once per round:
          1. First call  : initial user question
          2. Subsequent  : after appending tool results via request.add_message()
          3. Loop ends   : when response.has_answer() is True or response.has_error()
        """
        try:
            raw_message = self._llm_service.call_with_tool_list(
                messages=request.running_messages,
                tools=self._available_tools
            )
            return self._parse_llm_message(raw_message)

        except Exception as e:
            response = LLMResponse()
            response.add_error(str(e))
            return response

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _parse_llm_message(self, raw_message: dict) -> LLMResponse:
        """Parse the raw message dict returned by LLMService.call_with_tool_list()
        and populate a fresh LLMResponse.

        raw_message structure (model_dump output):
          {
            "role":       "assistant",
            "content":    <str | None>,
            "tool_calls": <list[dict] | None>
          }
        """
        response = LLMResponse()

        try:
            tool_calls = raw_message.get("tool_calls")
            content    = raw_message.get("content")

            if tool_calls:
                # LLM is requesting one or more tool calls
                response.add_tool_calls(tool_calls)

            elif content:
                # LLM has produced a final text answer
                response.add_answer(content)

            else:
                # Neither tool_calls nor content — unexpected state
                response.add_error("LLM returned an empty message: no content and no tool calls.")

        except Exception as e:
            response.add_error(f"Failed to parse LLM message: {str(e)}")

        return response

'''

[
    { "role": "system",    "content": "Role description Task description" },
    { "role": "user",      "content": "Question 1" },
    { "role": "assistant", "content": "Answer 1"   },
    { "role": "user",      "content": "Question 2" },
    { "role": "assistant", "content": "Answer 2"   },
    { "role": "user",      "content": "Question n" },
    { "role": "assistant", "content": null, "tool_calls": [{tool_1 details}, {tool_2 details}, {tool_3 details}]   },
    { "role": "tool",      "tool_call_id": "tool_1", "content": {tool_1 result} },
    { "role": "tool",      "tool_call_id": "tool_2", "content": {tool_2 result} },
    { "role": "tool",      "tool_call_id": "tool_3", "content": {tool_3 result} }
]

'''