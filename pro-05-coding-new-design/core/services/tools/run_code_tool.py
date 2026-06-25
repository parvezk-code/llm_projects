# core/services/tools/run_code_tool.py

from langchain_core.tools import tool
from core.services.tools.code_executor import CodeExecutor

_executor = CodeExecutor()


@tool
def run_code(code: str) -> str:
    """Execute Python code and return the output or error message."""
    return _executor.execute(code)

# core/services/tools/run_code_tool.py