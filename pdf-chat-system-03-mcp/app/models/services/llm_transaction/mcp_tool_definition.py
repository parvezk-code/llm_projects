# app/models/services/llm_transaction/mcp_tool_definition.py

from dataclasses import dataclass


@dataclass
class ParameterDefinition:
    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class MCPToolDefinition:
    name: str
    description: str
    parameters: list[ParameterDefinition]