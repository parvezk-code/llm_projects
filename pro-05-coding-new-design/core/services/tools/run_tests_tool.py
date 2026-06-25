# core/services/tools/run_tests_tool.py

import subprocess
import sys
from pathlib import Path
from langchain_core.tools import tool


@tool
def run_tests(test_file_path: str) -> str:
    """Run a pytest test file and return the results."""
    try:
        path = Path(test_file_path)
        if not path.exists():
            return f"Error: Test file not found at {test_file_path}"
        if not path.is_file():
            return f"Error: {test_file_path} is not a file."

        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file_path, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        return output if output else "No output from pytest."
    except subprocess.TimeoutExpired:
        return "Error: Test execution timed out after 30 seconds."
    except Exception as e:
        return f"Error running tests: {str(e)}"

# core/services/tools/run_tests_tool.py