# services/mcp/executor/response.py

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class MCPToolResponse:
    result: Optional[dict[str, Any]] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None

    def has_error(self) -> bool:
        return self.error_type is not None

    def has_result(self) -> bool:
        return self.result is not None
