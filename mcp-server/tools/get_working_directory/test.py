# tools/get_working_directory/test.py
# Run it from project root:
# python -m tools.get_working_directory.test

'''
Run from the root of the project:  python -m tools.get_working_directory.test
'''

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tools.get_working_directory.tool import get_working_directory


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(label: str, override_env: str | None = None):
    print(f"\n{'─' * 60}")
    print(f"TEST : {label}")

    if override_env is not None:
        os.environ["WORKING_DIRECTORY"] = override_env
        print(f"ENV  : WORKING_DIRECTORY={override_env}")
    else:
        os.environ.pop("WORKING_DIRECTORY", None)
        print(f"ENV  : WORKING_DIRECTORY=<not set, using default>")

    # Re-import settings fresh so env override takes effect
    import importlib
    import tools.get_working_directory.settings as settings_module
    importlib.reload(settings_module)

    import tools.get_working_directory.controller as controller_module
    importlib.reload(controller_module)

    import tools.get_working_directory.tool as tool_module
    importlib.reload(tool_module)

    result = tool_module.get_working_directory()

    print(f"OUTPUT:")
    for key, value in result.model_dump().items():
        print(f"  {key}: {value}")


# ── Test cases ────────────────────────────────────────────────────────────────

# 1. Default — uses ~/pdfs (may or may not exist on your machine)
run(
    label="Default working directory (~/pdfs)",
)

# 2. Valid directory — always exists
run(
    label="Valid directory (home dir)",
    override_env=str(os.path.expanduser("zz_test/work")),
)

# 3. Directory does not exist
run(
    label="Directory does not exist",
    override_env="/non/existent/path",
)

# 4. Path exists but is a file, not a directory
run(
    label="Path is a file, not a directory",
    override_env=os.path.abspath(__file__),
)