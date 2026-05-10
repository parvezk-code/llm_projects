from dataclasses import dataclass
from typing import Any


@dataclass
class MCPToolResult:
    success: bool
    data: Any = None
    error: str | None = None

    @classmethod
    def ok(cls, data: Any) -> "MCPToolResult":
        return cls(success=True, data=data, error=None)

    @classmethod
    def fail(cls, error: str) -> "MCPToolResult":
        return cls(success=False, data=None, error=error)
