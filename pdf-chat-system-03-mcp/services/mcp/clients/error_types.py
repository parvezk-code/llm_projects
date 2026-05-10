# services/mcp/clients/error_types.py

from typing import Literal

ErrorType = Literal[
    # client-side
    "ConnectionError",      # SyncConnection returned None — server unreachable
    "ToolCallError",        # Connected but tool call failed
    "ParseError",           # MCP result couldn't be parsed into response model
    "ValidationError",      # Bad input caught on client before call was made
    # server-side
    "DirectoryNotFound",    # Directory does not exist
    "NotADirectory",        # Path exists but is not a directory
    "UnexpectedError",      # Unhandled exception on server
]