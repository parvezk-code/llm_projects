# services/mcp/models/tool_definition.py

from pydantic import BaseModel, Field
from services.mcp.models.tool_parameter import ToolParameter


class ToolDefinition(BaseModel):
    name: str = Field(..., description="Tool name exposed to the LLM.")
    description: str = Field(..., description="Tool description for the LLM.")
    parameters: list[ToolParameter] = Field(default_factory=list)
