# app/models/services/llm_transaction/llm_transaction.py

from dataclasses import dataclass, field

from app.models.services.llm_transaction.chat_message import ChatMessage
from app.models.services.llm_transaction.mcp_tool_definition import MCPToolDefinition
from app.models.services.llm_transaction.tool_rounds import ToolRound


@dataclass
class LLMTransaction:
    history: list[ChatMessage]
    user_message: ChatMessage

    available_tools: list[MCPToolDefinition] = field(default_factory=list)
    tool_rounds: list[ToolRound] = field(default_factory=list)

    response: ChatMessage | None = None
    max_tool_rounds: int = 5