> Controller Architecture
---

###  MCP Services

```
get_documents_directory
    input: none
    output: directory path

list_pdfs_in_directory
    input: directory_path
    output: list of PDF files

read_pdf_content
    input: pdf_path
    output: PDF text

search_pdf_content
    --> returns only relevant pages/chunks from one or more PDFs
    
```
---




###  LLMTransaction

```

LLMTransaction
    ├── history
    ├── user_message
    ├── available_tools
    ├── tool_rounds
    │     ├── ToolRound 1
    │     │     ├── tool_calls
    │     │     └── tool_results
    │     ├── ToolRound 2
    │     │     ├── tool_calls
    │     │     └── tool_results
    │     └── ToolRound 3
    │           ├── tool_calls
    │           └── tool_results
    └── response

```