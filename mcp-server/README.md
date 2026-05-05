# MCP PDF Reader Server

An MCP server that extracts text from a PDF file and returns it with metadata. Built with FastMCP and PyMuPDF.

---

## What it does

Exposes a single MCP tool — `extract_pdf_text` — that receives a PDF file path and returns the full extracted text, page count, and resolved file path.

---

## Directory structure

```
pdf_reader/
├── main.py                          # Entry point
├── requirements.txt
│
├── server/
│   └── pdf_reader_server.py         # FastMCP instance, tool registration
│
├── tools/
│   └── extract_pdf_text_tool.py     # MCP boundary — builds request, calls controller,
│                                      serialises response to dict
│
├── controllers/
│   └── extract_pdf_text_controller.py  # Orchestrates validator + reader,
│                                         handles errors, returns response model
│
├── services/
│   ├── pdf_reader.py                # Raw PyMuPDF extraction — simple types only
│   └── pdf_validator.py             # Path, type, size, and empty file checks
│
├── models/
│   ├── request/
│   │   └── extract_pdf_text_request.py   # ExtractPDFTextRequest dataclass
│   └── response/
│       └── extract_pdf_text_response.py  # ExtractPDFTextResponse, Success, Error
│
├── utils/
│   └── result.py                    # Not used : Result base class with ok() and fail() factories
│
└── conf/
    └── settings.py                  # SERVER_NAME, MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS
```

---

## Setup

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Create a `conf/.env` file to override default settings:

```env
SERVER_NAME=pdf-reader-server
MAX_FILE_SIZE_MB=50
ALLOWED_EXTENSIONS=[".pdf"]
```

---

## Running the server

```bash
fastmcp run main.py
```

## Test the server
```
fastmcp inspect main.py

```

---

## Tool reference

### `extract_pdf_text`

Extracts all text from a PDF file.

**Input**

| Field | Type | Description |
|---|---|---|
| `pdf_path` | `str` | Absolute or relative path to the PDF file |

**Output — success**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `True` |
| `path` | `str` | Resolved absolute path to the file |
| `full_text` | `str` | All extracted text, whitespace trimmed |
| `page_count` | `int` | Number of pages in the PDF |

**Output — error**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `False` |
| `error_type` | `str` | `ValidationError` or `ExtractionError` |
| `error_message` | `str` | Human-readable description of the failure |

---

## Validation rules

- File must exist
- Path must point to a file, not a directory
- File extension must be in `ALLOWED_EXTENSIONS`
- File must not be empty
- File size must not exceed `MAX_FILE_SIZE_MB`
