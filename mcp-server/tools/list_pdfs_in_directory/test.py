# tools/list_pdfs_in_directory/test.py
# Run it from project root:
# python -m tools.list_pdfs_in_directory.test

'''
Run from the root of the project:  python -m tools.list_pdfs_in_directory.test
'''

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tools.list_pdfs_in_directory.tool import list_pdfs_in_directory


TOOL_DIR = os.path.dirname(__file__)
HOME_DIR = os.path.expanduser("~")


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(label: str, directory_path: str):
    print(f"\n{'─' * 60}")
    print(f"TEST : {label}")
    print(f"INPUT: {directory_path}")

    result = list_pdfs_in_directory(directory_path)

    print(f"OUTPUT:")
    for key, value in result.model_dump().items():
        if key == "pdf_files":
            print(f"  {key}: {value[:5]}{'...' if len(value) > 5 else ''}")
        else:
            print(f"  {key}: {value}")


# ── Test cases ────────────────────────────────────────────────────────────────

# 1. Valid directory — scans the tool's own directory (has .py files, no PDFs)
run(
    label="Valid directory, no PDFs present",
    directory_path=TOOL_DIR,
)

# 2. Valid directory — (may or may not have PDFs)
run(
    label="Valid directory",
    directory_path="zz_test/work",
)

# 3. Directory does not exist
run(
    label="Directory does not exist",
    directory_path="/non/existent/path",
)

# 4. Path is a file, not a directory
run(
    label="Path is a file, not a directory",
    directory_path=os.path.abspath(__file__),
)

# 5. Empty string input
run(
    label="Empty string input",
    directory_path="",
)
