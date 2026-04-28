# Step 10 — Identify Domain Controllers

## Domain Controllers

| Controller | Responsibility | Called by |
|---|---|---|
| `PDFService` | Load a PDF file from path, extract full text using PyMuPDF, return `PDFDocument` or raise error | `MainController` on `pdf_loaded` |
| `LLMService` | Build message payload, call OpenAI API, return assistant response text or raise error | `MainController` on `message_send_requested` |

---

## `PDFService` — Methods

| Method | Input | Output | Raises |
|---|---|---|---|
| `load(file_path)` | `str` — path to PDF file | `PDFDocument` | `PDFLoadError` if corrupt / password-protected |

---

## `LLMService` — Methods

| Method | Input | Output | Raises |
|---|---|---|---|
| `ask(request)` | `LLMRequest` | `str` — assistant response text | `LLMCallError` if API fails |
---
