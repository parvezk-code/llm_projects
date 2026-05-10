# services/llm/utils/openai_formatter.py

from app.models.services.llm_transaction.chat_message import ChatMessage
from services.mcp.models.mcp_tool_definition import ToolDefinition


class OpenAIFormatter:

    def format_message(self, message: ChatMessage) -> dict:
        return {
            "role": message.role,
            "content": message.content,
        }

    def _format_tool_definition(self, tool: ToolDefinition) -> dict:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {
                            "type": p.type,
                            "description": p.description,
                        }
                        for p in tool.parameters
                    },
                    "required": [
                        p.name for p in tool.parameters if p.required
                    ],
                },
            },
        }

    def format_tool_definitions(self, tools: list[ToolDefinition]) -> list[dict]:
        return [self._format_tool_definition(tool) for tool in tools]