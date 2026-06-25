# core/services/tools/code_executor.py

import subprocess
import sys


class CodeExecutor:
    """
    Executes Python code in a subprocess and returns stdout or an error message.
    Plain class with a timeout constant (matches the original Level 3 code).
    """

    TIMEOUT_SECONDS = 10

    def execute(self, code: str) -> str:
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_SECONDS,
            )
            if result.returncode == 0:
                return result.stdout or "Code executed successfully with no output."
            return f"Error:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return f"Error: Code execution timed out after {self.TIMEOUT_SECONDS} seconds."
        except Exception as e:
            return f"Error: {str(e)}"

# core/services/tools/code_executor.py