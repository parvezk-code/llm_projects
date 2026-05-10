# MCP PDF Reader Server

An MCP server that exposes tools to work with PDF files — list, read, and extract text. Built with FastMCP and PyMuPDF.

---

## What it does

Exposes four MCP tools:

| Tool | Description |
|---|---|
| `get_working_directory` | Returns the configured working directory where PDF files are present |
| `list_pdfs_in_directory` | Lists all PDF files in a given directory |
| `read_pdf_content` | Reads and returns the full text content of a PDF file |

---

## Directory structure

```
mcp-server/
├── README.md
├── main.py                          # Entry point
├── requirements.txt
│
├── server/
│   └── pdf_reader_server.py         # FastMCP instance and tool registration
│
└── tools/                           # Each tool is self-contained in its own directory
    │
    ├── get_working_directory/
    │   ├── .env                     # WORKING_DIRECTORY
    │   ├── settings.py              # WorkingDirectorySettings
    │   ├── response.py              # GetWorkingDirectoryResponse, Success, Error
    │   ├── controller.py            # Resolves and validates directory path
    │   ├── tool.py                  # MCP boundary
    │   └── test.py                  # Manual test runner
    │
    ├── list_pdfs_in_directory/
    │   ├── .env                     # ALLOWED_EXTENSIONS
    │   ├── settings.py              # ListPDFsSettings
    │   ├── request.py               # ListPDFsRequest
    │   ├── response.py              # ListPDFsResponse, Success, Error
    │   ├── directory_scanner.py     # Scans directory and filters PDF files
    │   ├── controller.py            # Validates path, calls scanner, builds response
    │   ├── tool.py                  # MCP boundary — validates input, calls controller
    │   └── test.py                  # Manual test runner
    │
    └── read_pdf_content/
        ├── .env                     # MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS
        ├── settings.py              # ReadPDFContentSettings
        ├── request.py               # ReadPDFContentRequest
        ├── response.py              # ReadPDFContentResponse, Success, Error
        ├── pdf_validator.py         # Path, type, size, and empty file checks
        ├── pdf_reader.py            # Raw PyMuPDF extraction
        ├── controller.py            # Orchestrates validator + reader, builds response
        ├── tool.py                  # MCP boundary — validates input, calls controller
        └── test.py                  # Manual test runner
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

Each tool has its own `.env` file for configuration. Defaults are already set — override only what you need:

```
tools/get_working_directory/.env
tools/list_pdfs_in_directory/.env
tools/read_pdf_content/.env
```

Example — change the working directory:
```env
# tools/get_working_directory/.env
WORKING_DIRECTORY=~/documents/pdfs
```

Example — increase file size limit:
```env
# tools/read_pdf_content/.env
MAX_FILE_SIZE_MB=100
```

---

## Running the server

```bash
fastmcp run main.py
```

## Inspect the server

```bash
fastmcp inspect main.py
```

---

## Testing tools manually

Each tool has its own `test.py`. Run from the project root:

```bash
python -m tools.get_working_directory.test
python -m tools.list_pdfs_in_directory.test
python -m tools.read_pdf_content.test
```

> Place a `test_doc.pdf` inside the relevant tool directory for PDF read/extract tests to pass.

---

## Tool reference

### `get_working_directory`

Returns the configured working directory where PDF files are present.

**Input:** none

**Output — success**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `True` |
| `directory_path` | `str` | Resolved absolute path to the working directory |

**Output — error**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `False` |
| `error_type` | `str` | `DirectoryNotFound`, `NotADirectory`, or `UnexpectedError` |
| `error_message` | `str` | Human-readable description of the failure |

---

### `list_pdfs_in_directory`

Lists all PDF files present in a given directory.

**Input**

| Field | Type | Description |
|---|---|---|
| `directory_path` | `str` | Absolute path to the directory to scan |

**Output — success**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `True` |
| `directory_path` | `str` | Resolved absolute path to the scanned directory |
| `pdf_files` | `list[str]` | Absolute paths of all PDF files found |
| `total_count` | `int` | Number of PDF files found |

**Output — error**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `False` |
| `error_type` | `str` | `DirectoryNotFound`, `NotADirectory`, `ValidationError`, or `UnexpectedError` |
| `error_message` | `str` | Human-readable description of the failure |

---

### `read_pdf_content`

Reads and returns the full text content of a PDF file.

**Input**

| Field | Type | Description |
|---|---|---|
| `pdf_path` | `str` | Absolute path to the PDF file |

**Output — success**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `True` |
| `pdf_path` | `str` | Resolved absolute path to the file |
| `full_text` | `str` | All extracted text, whitespace trimmed |
| `page_count` | `int` | Number of pages in the PDF |

**Output — error**

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `False` |
| `error_type` | `str` | `ValidationError` or `UnexpectedError` |
| `error_message` | `str` | Human-readable description of the failure |

---

## Validation rules

Applied by  `read_pdf_content`:

- File must exist
- Path must point to a file, not a directory
- File extension must be in `ALLOWED_EXTENSIONS`
- File must not be empty
- File size must not exceed `MAX_FILE_SIZE_MB`

Applied by `list_pdfs_in_directory` and `get_working_directory`:

- Path must exist
- Path must point to a directory, not a file