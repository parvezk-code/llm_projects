# services/graph/nodes/read_node.py

from pathlib import Path
from langchain_core.messages import AIMessage
from services.graph.state import GraphState


def read_node(state: GraphState) -> dict:
    project_path = state["project_path"]
    target_files = state.get("target_files", [])
    file_contents = {}

    path = Path(project_path)

    if target_files:
        for filename in target_files:
            file_path = path / filename
            if not file_path.exists():
                for found in path.rglob(filename):
                    file_path = found
                    break
            try:
                relative = str(file_path.relative_to(path))
                content = file_path.read_text(encoding="utf-8")
                file_contents[relative] = content
            except Exception:
                continue
    else:
        for file_path in sorted(path.rglob("*.py")):
            try:
                relative = str(file_path.relative_to(path))
                content = file_path.read_text(encoding="utf-8")
                file_contents[relative] = content
            except Exception:
                continue

    message = AIMessage(content=f"Read {len(file_contents)} file(s) from {project_path}.")
    return {
        "messages": [message],
        "file_contents": file_contents,
    }