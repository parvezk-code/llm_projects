# clients/error_types.py

from typing import Literal

ErrorType = Literal[
    "ConnectionError",      # SyncConnection returned None — server unreachable
    "ToolCallError",        # Connected but tool call failed
    "ParseError",           # MCP result couldn't be parsed into response model
    "ValidationError",      # Bad input caught before call was made
]