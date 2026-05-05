from typing import Any
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class MCPConnectionClient:
    """Thin MCP connection wrapper. All error handling is the caller's responsibility."""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self._streams_ctx = None
        self._session: ClientSession | None = None

    async def connect(self) -> None:
        self._streams_ctx = streamablehttp_client(self.server_url)
        read, write, _ = await self._streams_ctx.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if self._session is None:
            raise Exception("MCP client is not connected.")
        return await self._session.call_tool(tool_name, arguments)

    async def close(self) -> None:
        if self._session is not None:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception:
                pass
            finally:
                self._session = None

        if self._streams_ctx is not None:
            try:
                await self._streams_ctx.__aexit__(None, None, None)
            except Exception:
                pass
            finally:
                self._streams_ctx = None

    def is_connected(self) -> bool:
        return self._session is not None

    async def __aenter__(self) -> "MCPConnectionClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
