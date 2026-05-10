# services/mcp/mcp_tool_controller.py

import json
from typing import Any

from services.mcp.clients.client_sync import SyncConnection
from services.mcp.tool_registry import MCPToolRegistry
from services.mcp.models.mcp_tool_definition import ToolDefinition

class MCPToolController:
    """
    Generic controller for all MCP tool calls.

    Receives a tool name and arguments, delegates to SyncConnection,
    and always returns a plain dict — either the parsed MCP response
    or a structured error dict — ready to be sent to OpenAI as a
    tool_call result. Never raises exceptions.
    """

    def __init__(self, connection: SyncConnection) -> None:
        self._connection = connection
        self.list_of_tools = MCPToolRegistry().getAllMCPTools()

    def get_tools_list(self) -> list[ToolDefinition]:
        return self.list_of_tools

    def call(self, tool_name: str, arguments: dict[str, Any]) -> dict:
        result = self._connection.run(tool_name=tool_name, arguments=arguments)

        if result is None:
            return self._resolve_error()

        return self._parse(result)

    # ------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------

    def _resolve_error(self) -> dict:
        
        fail_message = {}
        fail_message["success"] = False
        
        if not self._connection.connected:
            fail_message["error_type"] = "ConnectionError"
            fail_message["error_message"] = "MCP server is not reachable"
        elif not self._connection.tool_called:
            fail_message["error_type"] = "ToolExecutionError"
            fail_message["error_message"] = "Connected to MCP server but tool execution failed"
        else:
            fail_message["error_type"] = "EmptyResultError"
            fail_message["error_message"] = "Tool was called but returned no content"

        return fail_message

    def _parse(self, result: Any) -> dict:
        """
        Extract text from the first content block and parse it as JSON.
        MCP always returns a CallToolResult with content[0].text as a
        JSON string, so this is sufficient for all tools.
        """
        isIndexError = True
        try:
            text = result.content[0].text
            isIndexError = False
            return json.loads(text)
        except Exception as e:
            if isIndexError :
                return {
                    "success": False,
                    "error_type": "ParseError",
                    "error_message": "MCP response contained no content blocks",
                }
            else:
                return {
                    "success": False,
                    "error_type": "ParseError",
                    "error_message": "MCP response content was not valid JSON",
                }