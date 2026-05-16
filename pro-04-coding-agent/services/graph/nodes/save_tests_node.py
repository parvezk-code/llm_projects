# services/graph/nodes/save_tests_node.py

from pathlib import Path
from langchain_core.messages import AIMessage
from services.graph.state import GraphState


def save_tests_node(state: GraphState) -> dict:
    project_path = state["project_path"]
    test_code = state["test_code"]

    test_file_path = str(Path(project_path) / "test_generated.py")

    try:
        Path(test_file_path).write_text(test_code, encoding="utf-8")
        message = AIMessage(content=f"Tests saved to {test_file_path}")
    except Exception as e:
        message = AIMessage(content=f"Error saving tests: {str(e)}")
        test_file_path = ""

    return {
        "messages": [message],
        "test_file_path": test_file_path,
    }