# services/tools/read_file/tool.py

from pathlib import Path
from langchain_core.tools import tool


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a file at the given path and return it as a string."""
    try:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File not found at {file_path}"
        if not path.is_file():
            return f"Error: {file_path} is not a file."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"