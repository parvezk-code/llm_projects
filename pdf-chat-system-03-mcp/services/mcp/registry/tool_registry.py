# services/mcp/registry/tool_registry.py

from pathlib import Path
from services.mcp.models.tool_definition import ToolDefinition


class MCPToolRegistry:

    def __init__(self):
        dir_01 = Path(__file__).parent / "tools_json"       # now resolves to registry/tools_json/
        self._list_of_directories = [dir_01]

    def getAllMCPTools(self) -> list[ToolDefinition]:
        all_tools: list[ToolDefinition] = []

        for directory in self._list_of_directories:
            tools_from_directory = self.load_tools_from_directory(directory)
            all_tools.extend(tools_from_directory)

        return all_tools

    def load_tools_from_directory(self, directory: Path) -> list[ToolDefinition]:
        json_files = sorted(Path(directory).glob("*.json"))

        tools: list[ToolDefinition] = []

        for file_path in json_files:
            json_text = file_path.read_text(encoding="utf-8")
            tool_definition = ToolDefinition.model_validate_json(json_text)
            tools.append(tool_definition)

        return tools
