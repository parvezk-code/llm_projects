# services/mcp/clients/client_sync.py

import asyncio
from typing import Any

from services.mcp.clients.client_async import MCPConnectionClient
from services.mcp.exceptions import MCPConnectionError, MCPToolExecutionError


class SyncConnection:

    def __init__(self, server_url: str):
        self.server_url = server_url

    def run(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        return asyncio.run(self._execute(tool_name, arguments))

    async def _execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        client = MCPConnectionClient(self.server_url)

        try:
            await client.connect()
        except Exception as e:
            await client.close()
            raise MCPConnectionError("MCP server is not reachable") from e

        try:
            result = await client.call_tool(tool_name, arguments)
        except Exception as e:
            await client.close()
            raise MCPToolExecutionError("Connected but tool execution failed") from e

        await client.close()
        return result
