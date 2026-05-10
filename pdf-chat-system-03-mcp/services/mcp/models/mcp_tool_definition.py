# services/mcp/models/mcp_tool_definition.py

from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    name: str = Field(..., description="Parameter name expected by the tool.")
    type: str = Field(..., description="JSON schema type, for example: string, integer, boolean.")
    description: str = Field(..., description="Description of the parameter for the LLM.")
    required: bool = Field(default=True, description="Whether this parameter is required.")


class ToolDefinition(BaseModel):
    name: str = Field(..., description="Tool name exposed to the LLM.")
    description: str = Field(..., description="Tool description for the LLM.")
    parameters: list[ToolParameter] = Field(default_factory=list)