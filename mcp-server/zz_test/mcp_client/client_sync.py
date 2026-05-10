# mcp_connection/client_sync.py

import asyncio
from typing import Any

from clients.client_async import MCPConnectionClient


class SyncConnection:

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.connected: bool = False
        self.tool_called: bool = False
        self.closed: bool = False

    def _reset_status(self) -> None:
        self.connected = False
        self.tool_called = False
        self.closed = False

    def _run(self, tool_name: str, arguments: dict[str, Any]) -> Any | None:
        return asyncio.run(self._execute(tool_name, arguments))

    async def _execute(self, tool_name: str, arguments: dict[str, Any]) -> Any | None:
        self._reset_status()
        client = MCPConnectionClient(self.server_url)

        try:
            await client.connect()
            self.connected = True

            result = await client.call_tool(tool_name, arguments)
            self.tool_called = True

            return result

        except Exception:
            return None

        finally:
            await client.close()
            self.closed = True