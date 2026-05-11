# services/mcp/executor/request.py

from typing import Any
from pydantic import BaseModel, Field


class MCPToolRequest(BaseModel):
    tool_name: str = Field(..., min_length=1, description="Name of the MCP tool to call.")
    arguments: dict[str, Any] = Field(default_factory=dict, description="Arguments to pass to the tool.")
