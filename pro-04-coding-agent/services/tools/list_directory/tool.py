# services/tools/list_directory/tool.py

from pathlib import Path
from langchain_core.tools import tool


@tool
def list_directory(directory_path: str) -> str:
    """List all files and subdirectories in a directory recursively."""
    try:
        path = Path(directory_path)
        if not path.exists():
            return f"Error: Directory not found at {directory_path}"
        if not path.is_dir():
            return f"Error: {directory_path} is not a directory."

        entries = sorted(path.rglob("*"))
        lines = []
        for entry in entries:
            relative = entry.relative_to(path)
            if entry.is_dir():
                lines.append(f"[dir]  {relative}/")
            else:
                lines.append(f"[file] {relative}")

        if not lines:
            return "Directory is empty."

        return "\n".join(lines)
    except Exception as e:
        return f"Error listing directory: {str(e)}"