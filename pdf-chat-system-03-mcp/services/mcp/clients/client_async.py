# services/mcp/clients/client_async.py

import asyncio
import logging
from typing import Any
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

log = logging.getLogger(__name__)


class MCPConnectionClient:

    def __init__(self, server_url: str):
        self.server_url   = server_url
        self._streams_ctx = None
        self._session     = None
        self._initialized = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        await self._probe_tcp()          # fast-fail before anyio is involved
        
        self._streams_ctx = streamablehttp_client(self.server_url)
        read, write, _    = await self._streams_ctx.__aenter__()
        self._session     = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        self._initialized = True

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        if not self._initialized:
            return None
        return await self._session.call_tool(tool_name, arguments)

    async def close(self) -> None:
        if self._session is not None:
            try:
                await self._session.__aexit__(None, None, None)
            except Exception as e:
                log.debug("Suppressed session close error: %s", e)
            finally:
                self._session     = None
                self._initialized = False

        if self._streams_ctx is not None:
            try:
                await self._streams_ctx.__aexit__(None, None, None)
            except Exception as e:
                log.debug("Suppressed stream close error: %s", e)
            finally:
                self._streams_ctx = None

    def is_connected(self) -> bool:
        return self._initialized

    async def __aenter__(self) -> "MCPConnectionClient":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    async def _probe_tcp(self) -> None:
        """
        Open and immediately close a raw TCP connection to the MCP server.
        Raises ConnectionRefusedError fast — before streamablehttp_client
        is entered — so anyio's task group is never created and asyncio.run()
        can tear down cleanly.
        """
        from urllib.parse import urlparse

        parsed = urlparse(self.server_url)
        host   = parsed.hostname
        port   = parsed.port or (443 if parsed.scheme == "https" else 80)

        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=5.0
            )
            writer.close()
            await writer.wait_closed()

        except (OSError, asyncio.TimeoutError) as e:
            raise ConnectionRefusedError(
                f"MCP server not reachable at {host}:{port} — {e}"
            ) from e