# services/mcp/executor/controller.py

import json

from services.mcp.clients.client_sync import SyncConnection
from services.mcp.executor.request import MCPToolRequest
from services.mcp.executor.response import MCPToolResponse
from services.mcp.registry.tool_registry import MCPToolRegistry
from services.mcp.models.tool_definition import ToolDefinition
from services.mcp.exceptions import MCPConnectionError, MCPToolExecutionError, MCPParseError


class MCPToolController:
    """
    Generic controller for all MCP tool calls.
    Receives MCPToolRequest, calls SyncConnection directly,
    catches exceptions, parses result, returns MCPToolResponse.
    Never raises exceptions.
    """

    def __init__(self, connection: SyncConnection) -> None:
        self._connection = connection
        self._tools = MCPToolRegistry().getAllMCPTools()

    # --- Called by MainController ---

    def get_tools_list(self) -> list[ToolDefinition]:
        return self._tools

    def call(self, request: MCPToolRequest) -> MCPToolResponse:
        try:
            raw = self._connection.run(
                tool_name=request.tool_name,
                arguments=request.arguments
            )
            return self._parse(raw)

        except MCPConnectionError as e:
            return MCPToolResponse(
                error_type="ConnectionError",
                error_message=str(e)
            )
        except MCPToolExecutionError as e:
            return MCPToolResponse(
                error_type="ToolExecutionError",
                error_message=str(e)
            )
        except MCPParseError as e:
            return MCPToolResponse(
                error_type="ParseError",
                error_message=str(e)
            )
        except Exception as e:
            return MCPToolResponse(
                error_type="UnexpectedError",
                error_message=str(e)
            )

    # ------------------------------------------------------------------
    # private
    # ------------------------------------------------------------------

    def _parse(self, raw) -> MCPToolResponse:
        try:
            text = raw.content[0].text
        except Exception:
            raise MCPParseError("MCP response contained no content blocks")

        try:
            parsed = json.loads(text)
            return MCPToolResponse(result=parsed)
        except Exception:
            raise MCPParseError("MCP response content was not valid JSON")