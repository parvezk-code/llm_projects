# services/graph/nodes/run_tests_node.py

import subprocess
import sys
from langchain_core.messages import AIMessage
from services.graph.state import GraphState


def run_tests_node(state: GraphState) -> dict:
    test_file_path = state.get("test_file_path", "")

    if not test_file_path:
        message = AIMessage(content="No test file to run.")
        return {"messages": [message], "test_results": "No test file found."}

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file_path, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        test_results = result.stdout + result.stderr
        message = AIMessage(content=f"Test results:\n```\n{test_results}\n```")
    except subprocess.TimeoutExpired:
        test_results = "Error: Test execution timed out after 30 seconds."
        message = AIMessage(content=test_results)
    except Exception as e:
        test_results = f"Error running tests: {str(e)}"
        message = AIMessage(content=test_results)

    return {
        "messages": [message],
        "test_results": test_results,
    }