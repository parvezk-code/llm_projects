# test_extract.py
'''
Run from inside pdf_reader/ directory:  python test_extract.py
'''

# test_extract.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.extract_pdf_text_tool import extract_pdf_text


TEST_DIR = os.path.dirname(__file__)
VALID_PDF_PATH = os.path.join(TEST_DIR, "test_doc.pdf")
VALID_TXT_PATH = os.path.join(TEST_DIR, "test_doc.txt")
INVALID_FILE_PATH = os.path.join(TEST_DIR, "test.txt")
DIRECTORY_PATH = TEST_DIR

# ── Test cases ────────────────────────────────────────────────────────────────

def run(label: str, pdf_path: str):
    print(f"\n{'─' * 60}")
    print(f"TEST : {label}")
    print(f"INPUT: {pdf_path}")
    result = extract_pdf_text(pdf_path)
    print(f"OUTPUT:")
    for key, value in result.items():
        if key == "full_text" and value:
            print(f"  {key}: {value[:200]}...")   # truncate long text
        else:
            print(f"  {key}: {value}")


# ── Run tests ─────────────────────────────────────────────────────────────────

# 1. Valid PDF — replace with a real path on your machine
run(
    label="Valid PDF",
    pdf_path=VALID_PDF_PATH
)

# 2. File does not exist
run(
    label="File not found",
    pdf_path=INVALID_FILE_PATH
)

# 3. Not a PDF
run(
    label="Wrong file type",
    pdf_path=VALID_TXT_PATH
)

# 4. Path is a directory
run(
    label="Path is a directory",
    pdf_path=DIRECTORY_PATH
)