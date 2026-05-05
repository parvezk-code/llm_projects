import asyncio
from typing import Any

from services.mcp.mcp_connection_client import MCPConnectionClient
from services.mcp.models.mcp_tool_result import MCPToolResult


class MCPClientController:
    """Synchronous wrapper used by MainController."""

    def __init__(self, server_url: str):
        self.server_url = server_url

    def call_tool_sync(self, tool_name: str, arguments: dict[str, Any]) -> MCPToolResult:
        try:
            return asyncio.run(self._call_tool_async(tool_name, arguments))
        except Exception as e:
            return MCPToolResult.fail(f"Unexpected error: {str(e)}")

    async def _call_tool_async(self, tool_name: str, arguments: dict[str, Any]) -> MCPToolResult:
        client = MCPConnectionClient(self.server_url)

        try:
            await client.connect()
        except Exception as e:
            return MCPToolResult.fail(f"Connection failed: {str(e)}")

        try:
            result = await client.call_tool(tool_name, arguments)
            return MCPToolResult.ok(result)
        except Exception as e:
            return MCPToolResult.fail(f"Tool call failed: {str(e)}")
        finally:
            await client.close()
