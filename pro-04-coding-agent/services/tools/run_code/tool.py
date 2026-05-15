# services/tools/run_code/tool.py

from langchain_core.tools import tool
from services.tools.run_code.executor import CodeExecutor

_executor = CodeExecutor()


@tool
def run_code(code: str) -> str:
    """Execute Python code and return the output or error message."""
    return _executor.execute(code)