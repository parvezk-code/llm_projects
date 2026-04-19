# PDF Chat System

A simple Streamlit app that lets you upload a PDF and chat with an OpenAI model about its contents. Text is extracted locally with [PyPDF](https://pypi.org/project/pypdf/); if the PDF is a scan (no embedded text), it falls back to OCR via [Tesseract](https://github.com/tesseract-ocr/tesseract) + [pdf2image](https://pypi.org/project/pdf2image/).

## Features

- Browser-based chat UI (Streamlit).
- Drop-in PDF upload.
- Automatic text extraction, with OCR fallback for scanned PDFs.
- Full PDF text is stuffed into the system prompt (simple v1 — no RAG).
- Model and API key configured via environment variables.

## Requirements

- Python 3.10+
- An OpenAI API key (https://platform.openai.com/api-keys)
- For OCR fallback on scanned PDFs:
  - **macOS:** `brew install tesseract poppler`
  - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr poppler-utils`
  - **Windows:** install [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and [Poppler](https://github.com/oschwartz10612/poppler-windows/releases), then make sure both are on your `PATH`.

OCR tooling is only needed if you plan to upload scanned/image-only PDFs. Text-based PDFs work without it.

## Setup

```bash
# 1. Clone the repo and enter it
git clone <repo-url> pdf-chat-system
cd pdf-chat-system

# 2. Create and activate a virtualenv
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. (Optional) Install OCR tooling if you need the scanned-PDF fallback
#    macOS:
brew install tesseract poppler
#    Ubuntu/Debian:
# sudo apt-get install tesseract-ocr poppler-utils

# 5. Configure environment variables
cp .env.example .env
# then open .env and set:
#   OPENAI_API_KEY=sk-...
#   OPENAI_MODEL=gpt-4o-mini        # or gpt-4o, gpt-4-turbo, etc.
#   OPENAI_BASE_URL=                # optional; leave blank for OpenAI's default
```

### Using OpenRouter (or any OpenAI-compatible endpoint)

The client uses the OpenAI SDK, which works with any OpenAI-compatible API. To point it at [OpenRouter](https://openrouter.ai/):

```
OPENAI_API_KEY=sk-or-v1-...
OPENAI_MODEL=openai/gpt-4o-mini          # OpenRouter prefixes provider/model
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

The same pattern works for local runners that expose an OpenAI-compatible API (Ollama, LM Studio, vLLM, etc.) — set `OPENAI_BASE_URL` to their endpoint and `OPENAI_MODEL` to whatever model they serve.

### Sign in with ChatGPT (Plus/Pro)

As an alternative to an API key, the sidebar has a "Sign in with ChatGPT" button that authenticates against `auth.openai.com` via OAuth (PKCE), persists tokens to `./.pdf-chat/auth.json`, and routes requests to the Codex responses endpoint that a ChatGPT subscription covers.

Caveats — read before using:

- This reuses the OpenAI Codex CLI's public OAuth client ID and hits `https://chatgpt.com/backend-api/codex/responses`, which is not a published public API. Both things are ToS grey areas. OpenAI could break or disallow this at any time. Use for personal tooling only.
- Only Codex-family models are reachable via this path: `gpt-5.1-codex`, `gpt-5.1-codex-mini`, `gpt-5.1-codex-max`, `gpt-5.2-codex`, `gpt-5.3-codex`. Pick one in the sidebar after signing in.
- The `OPENAI_MODEL` env var does not apply in this mode.
- To sign out, click **Sign out**, or delete `./.pdf-chat/auth.json`.

## Run

```bash
streamlit run app.py
```

Streamlit will open the app at http://localhost:8501. Upload a PDF, wait for extraction, and start asking questions.

## How it works

```
┌─────────────────────┐
│   Streamlit app.py  │   ← file uploader + chat UI
└──────────┬──────────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌──────────┐
│extractor│  │llm_client│
│ pypdf → │  │ OpenAI   │
│ OCR     │  │ Chat     │
│ fallback│  │ Completns│
└─────────┘  └──────────┘
```

- `pdf_extractor.py` — `extract(pdf_bytes)` returns `ExtractedDoc(text, page_count, used_ocr)`. Tries PyPDF first; if the extracted text is too short (indicator of a scanned PDF), it rasterizes pages with `pdf2image` and OCRs them with `pytesseract`.
- `llm_client.py` — thin wrapper around `openai.chat.completions.create`. Reads `OPENAI_API_KEY` and `OPENAI_MODEL` from the environment (via `python-dotenv`). Truncates PDF text to stay within a ~100k-token budget.
- `app.py` — Streamlit UI. Caches the extracted doc in `st.session_state` keyed by file hash so switching prompts doesn't re-extract. Sidebar has "Clear conversation" and "Remove PDF" buttons.

## Project layout

```
pdf-chat-system/
├── app.py              # Streamlit entrypoint
├── pdf_extractor.py    # PyPDF + OCR fallback
├── llm_client.py       # OpenAI chat wrapper
├── requirements.txt
├── .env.example
└── .gitignore
```

## Troubleshooting

- **`OPENAI_API_KEY is not set`** — make sure you copied `.env.example` to `.env` and filled in the key, and that you ran Streamlit from the project root (so `.env` is picked up).
- **`OPENAI_MODEL is not set`** — set it in `.env` (e.g. `OPENAI_MODEL=gpt-4o-mini`).
- **`Tesseract binary not found`** — install it for your OS (see Requirements). Only hit when a scanned PDF triggers OCR fallback.
- **`OCR fallback failed while rasterizing the PDF`** — Poppler isn't installed or isn't on `PATH`.
- **Truncation warning on large PDFs** — v1 stuffs the whole PDF into context. For very large documents you'll want RAG (chunking + vector search) — not yet implemented.

## Limitations (v1)

- No RAG / chunking — large PDFs get truncated.
- One PDF per session.
- No response streaming.
- No conversation persistence across sessions.
- No auth / multi-user support.
