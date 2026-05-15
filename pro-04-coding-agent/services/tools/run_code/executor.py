# services/tools/run_code/executor.py

import subprocess
import sys


class CodeExecutor:

    def execute(self, code: str) -> str:
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                return result.stdout or "Code executed successfully with no output."
            return f"Error:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out after 10 seconds."
        except Exception as e:
            return f"Error: {str(e)}"