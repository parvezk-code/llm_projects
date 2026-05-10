# tools/read_pdf_content/test.py
# Run it from project root:
# python -m tools.read_pdf_content.test

'''
Run from the root of the project:  python -m tools.read_pdf_content.test
'''

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tools.read_pdf_content.tool import read_pdf_content


# TOOL_DIR = os.path.dirname(__file__)
TOOL_DIR = "zz_test/work"
VALID_PDF_PATH = os.path.join(TOOL_DIR, "test_doc.pdf")
INVALID_EXT_PATH = os.path.join(TOOL_DIR, "test_doc.txt")
DIRECTORY_PATH = TOOL_DIR


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(label: str, pdf_path: str):
    print(f"\n{'─' * 60}")
    print(f"TEST : {label}")
    print(f"INPUT: {pdf_path}")

    result = read_pdf_content(pdf_path)

    print(f"OUTPUT:")
    for key, value in result.model_dump().items():
        if key == "full_text" and value:
            print(f"  {key}: {value[:200]}...")
        else:
            print(f"  {key}: {value}")


# ── Test cases ────────────────────────────────────────────────────────────────

# 1. Valid PDF — place a test_doc.pdf inside tools/read_pdf_content/
run(
    label="Valid PDF",
    pdf_path=VALID_PDF_PATH,
)

# 2. File does not exist
run(
    label="File does not exist",
    pdf_path="/non/existent/file.pdf",
)

# 3. Wrong file extension
run(
    label="Wrong file extension",
    pdf_path=INVALID_EXT_PATH,
)

# 4. Path is a directory
run(
    label="Path is a directory",
    pdf_path=DIRECTORY_PATH,
)

# 5. Empty string input
run(
    label="Empty string input",
    pdf_path="",
)
