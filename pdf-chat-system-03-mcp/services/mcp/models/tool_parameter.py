# services/mcp/models/tool_parameter.py

from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    name: str = Field(..., description="Parameter name expected by the tool.")
    type: str = Field(..., description="JSON schema type, for example: string, integer, boolean.")
    description: str = Field(..., description="Description of the parameter for the LLM.")
    required: bool = Field(default=True, description="Whether this parameter is required.")
