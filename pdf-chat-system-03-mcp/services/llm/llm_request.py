# services/llm/llm_request.py
import json
from app.models.services.llm_transaction.chat_message import ChatMessage

class LLMRequest:

    def __init__(self, system_prompt: str, chat_history: list[ChatMessage], user_question: str):
        self._system_prompt   = system_prompt
        self.running_messages = self._build_initial_messages(chat_history, user_question)

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _build_initial_messages(self, chat_history: list[ChatMessage], user_question: str) -> list[dict]:
        """Build the initial running_messages list:
           [system_prompt] + chat_history + [new user question]
        """
        messages = []

        # System prompt always comes first
        messages.append({"role": "system", "content": self._system_prompt})

        # Append previous conversation turns
        # messages.extend(chat_history)
        for msg in chat_history:
            messages.append({"role": msg.role, "content": msg.content})

        # Append the new user question
        messages.append({"role": "user", "content": user_question})

        return messages

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def add_message(self, message: dict) -> None:
        """Append a single message dict to running_messages.
        
        Called each tool round to append:
          - the assistant tool-call message
          - individual tool result messages
        """
        self.running_messages.append(message)

    def add_tool_result(self, tool_call_id: str, result: dict) -> None:
        message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": json.dumps(result),
        }
        self.running_messages.append(message)


'''
Sample  running_message is as follows

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