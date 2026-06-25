# core/services/tools/write_file_tool.py

from pathlib import Path
from langchain_core.tools import tool


@tool
def write_file(file_path: str, content: str) -> str:
    """Write content to a file at the given path. Creates the file if it does not exist."""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Successfully written to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# core/services/tools/write_file_tool.py