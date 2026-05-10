
> MCP Tools 

| Tool Name                 | Input                      | Output                                               |
| ------------------------- | -------------------------- | ---------------------------------------------------- |
| get_documents_directory | none                       | Directory path                                       |
| list_pdfs_in_directory  | directory_path           | List of PDF file paths or file names                 |
| read_pdf_content        | pdf_path                | Full extracted text from the PDF                     |

---

> MCP Tools : planned for future

| Tool Name                 | Input                      | Output                                               |
| ------------------------- | -------------------------- | ---------------------------------------------------- |
| search_pdf_content      | Query + filters (optional) | Relevant pages/chunks/snippets from one or more PDFs |

---

# Directory structure

```

mcp-server/
├── README.md
├── main.py
├── requirements.txt
│
├── server/
│   └── pdf_reader_server.py
│
└── tools/
    │
    ├── get_working_directory/
    |   ├── .env
    │   ├── response.py
    │   ├── settings.py
    │   ├── controller.py
    │   ├── tool.py
    │   └── test.py
    │
    ├── list_pdfs_in_directory/
    |   ├── .env
    │   ├── request.py
    │   ├── response.py
    │   ├── directory_scanner.py
    │   ├── settings.py
    │   ├── controller.py
    │   ├── tool.py
    │   └── test.py
    │
    └── read_pdf_content/
        ├── .env
        ├── request.py
        ├── response.py
        ├── pdf_reader.py
        ├── pdf_validator.py
        ├── settings.py
        ├── controller.py
        ├── tool.py
        └── test.py


```

## File Responsibilities

> Main Server

| File | Contains |
|---|---|
| main.py | Entry point. Starts the MCP server by importing and running the FastMCP instance. |
| server/pdf_reader_server.py | Creates the FastMCP instance. Registers all three tools: get_working_directory, list_pdfs_in_directory, read_pdf_content. |

---

> Tool: get_working_directory

| File | Contains |
|---|---|
| tool.py | Tool function registered with FastMCP. Calls controller and returns response. |
| controller.py | Resolves and validates the working directory path from settings. Returns success or error response. |
| response.py | Pydantic models: GetWorkingDirectoryResponse (base), GetWorkingDirectorySuccessResponse, GetWorkingDirectoryErrorResponse. |
| settings.py | Pydantic settings model. Reads WORKING_DIRECTORY from .env. |
| .env | Environment variable: WORKING_DIRECTORY. |
| test.py | Standalone tests for the tool's controller logic. |

---

> Tool: list_pdfs_in_directory

| File | Contains |
|---|---|
| tool.py | Tool function registered with FastMCP. Validates input via ListPDFsRequest, calls controller, returns response. |
| controller.py | Validates directory path exists and is a directory. Calls DirectoryScanner. Returns success or error response. |
| request.py | Pydantic model: ListPDFsRequest. Validates directory_path — min length 1. |
| response.py | Pydantic models: ListPDFsResponse (base), ListPDFsSuccessResponse, ListPDFsErrorResponse. |
| directory_scanner.py | DirectoryScanner class. Scans a directory and returns sorted list of files matching allowed extensions. |
| settings.py | Pydantic settings model. Reads ALLOWED_EXTENSIONS from .env. |
| .env | Environment variable: ALLOWED_EXTENSIONS. |
| test.py | Standalone tests for the tool's controller and scanner logic. |

---

> Tool: read_pdf_content

| File | Contains |
|---|---|
| tool.py | Tool function registered with FastMCP. Validates input via ReadPDFContentRequest, calls controller, returns response. |
| controller.py | Calls PDFValidator then PDFReader. Returns success with extracted text and page count, or error response. |
| request.py | Pydantic model: ReadPDFContentRequest. Validates pdf_path — min length 1. |
| response.py | Pydantic models: ReadPDFContentResponse (base), ReadPDFContentSuccessResponse, ReadPDFContentErrorResponse. |
| pdf_validator.py | PDFValidator class. Checks path exists, is a file, has allowed extension, is non-empty, and is within max file size. |
| pdf_reader.py | PDFReader class. Opens PDF with PyMuPDF (fitz), extracts full text and page count. |
| settings.py | Pydantic settings model. Reads MAX_FILE_SIZE_MB and ALLOWED_EXTENSIONS from .env. |
| .env | Environment variables: MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS. |
| test.py | Standalone tests for the tool's validator, reader, and controller logic. |