# Chat PDF App — Setup & Run Guide

---

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key

---

## 1. Clone or Download the Project

Move into the project root — the folder that contains `conf/`, `core/`, `ui/`,
`desktop/`, `desktop_local/`, and `requirements.txt`.

```bash
cd chat_pdf
```

> **Important:** every command below must be run from this project root. The
> app loads its configuration using paths relative to the root, and it is
> started as a module (`-m`), so running from another folder will fail.

---

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `PyQt6` (UI), `openai` (LLM client), `PyMuPDF` (PDF text
extraction), and `pydantic-settings` (configuration).

---

## 4. Configure Your OpenAI Key

Configuration lives in `conf/env/`. Settings are split into two files:

- `conf/env/.env.openAI` — **non-secret** settings (model, temperature, max
  tokens). Already provided; edit if you want different values.
- `conf/env/.env.local` — **your secret** key. This file is gitignored and is
  **not** included; you create it.

Create `conf/env/.env.local` with your key:

```
api_key=sk-your-api-key-here
```

You can copy `conf/env/.env.openAI.example` as a starting point. If you prefer,
you may also override the model there:

```
api_key=sk-your-api-key-here
model=gpt-4.1-mini
```

> The app will refuse to start until a valid `api_key` is provided. `.env.local`
> takes priority over `.env.openAI`.

---

## 5. Run the App

From the project root:

```bash
python -m desktop_local.main
```

---

## 6. Using the App

| Step | Action |
|---|---|
| 1 | Click **Upload PDF** to select a PDF file |
| 2 | Wait for the filename to appear in the toolbar |
| 3 | Type a question in the input box |
| 4 | Press **Enter** or click **Send** |
| 5 | Wait for the AI response to appear |
| 6 | Click **Clear** to reset the conversation |
| 7 | Click **Upload PDF** again to load a different PDF |

> **Note:** while the AI response is being generated, the window may appear to
> freeze for a few seconds. This is expected in the current version — the
> request runs on the UI thread.

---

## 7. Troubleshooting — If `pip install` Fails

If `pip install -r requirements.txt` fails, or pip stops working after a
previously successful install, the virtual environment is likely corrupted.
Recreate it from scratch, running these commands from the project root:

```bash
# Step 1 — navigate to the project root
cd /path/to/chat_pdf

# Step 2 — deactivate the current venv if active
deactivate

# Step 3 — delete the broken venv
rm -rf .venv

# Step 4 — recreate the venv
python3 -m venv .venv

# Step 5 — activate the new venv
source .venv/bin/activate

# Step 6 — install dependencies
pip install -r requirements.txt
```

---

## 8. Troubleshooting — Common Problems

| Problem | Solution |
|---|---|
| `Configuration error` / `api_key field required` | Create `conf/env/.env.local` containing `api_key=sk-...` |
| `Could not load PDF` | File may be corrupt, password-protected, or not a valid PDF |
| `Could not get a response` | Check your internet connection and that your API key is valid |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside your virtual environment |
| `No module named desktop_local` | Run from the project root using `python -m desktop_local.main` |
| App window does not appear | Ensure PyQt6 installed correctly for your OS |# Chat PDF App — Setup & Run Guide

---

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key

---

## 1. Clone or Download the Project

Move into the project root — the folder that contains `conf/`, `core/`, `ui/`,
`desktop/`, `desktop_local/`, and `requirements.txt`.

```bash
cd chat_pdf
```

> **Important:** every command below must be run from this project root. The
> app loads its configuration using paths relative to the root, and it is
> started as a module (`-m`), so running from another folder will fail.

---

## 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

**macOS / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `PyQt6` (UI), `openai` (LLM client), `PyMuPDF` (PDF text
extraction), and `pydantic-settings` (configuration).

---

## 4. Configure Your OpenAI Key

Configuration lives in `conf/env/`. Settings are split into two files:

- `conf/env/.env.openAI` — **non-secret** settings (model, temperature, max
  tokens). Already provided; edit if you want different values.
- `conf/env/.env.local` — **your secret** key. This file is gitignored and is
  **not** included; you create it.

Create `conf/env/.env.local` with your key:

```
api_key=sk-your-api-key-here
```

You can copy `conf/env/.env.openAI.example` as a starting point. If you prefer,
you may also override the model there:

```
api_key=sk-your-api-key-here
model=gpt-4.1-mini
```

> The app will refuse to start until a valid `api_key` is provided. `.env.local`
> takes priority over `.env.openAI`.

---

## 5. Run the App

From the project root:

```bash
python -m desktop_local.main
```

---

## 6. Using the App

| Step | Action |
|---|---|
| 1 | Click **Upload PDF** to select a PDF file |
| 2 | Wait for the filename to appear in the toolbar |
| 3 | Type a question in the input box |
| 4 | Press **Enter** or click **Send** |
| 5 | Wait for the AI response to appear |
| 6 | Click **Clear** to reset the conversation |
| 7 | Click **Upload PDF** again to load a different PDF |

> **Note:** while the AI response is being generated, the window may appear to
> freeze for a few seconds. This is expected in the current version — the
> request runs on the UI thread.

---

## 7. Troubleshooting — If `pip install` Fails

If `pip install -r requirements.txt` fails, or pip stops working after a
previously successful install, the virtual environment is likely corrupted.
Recreate it from scratch, running these commands from the project root:

```bash
# Step 1 — navigate to the project root
cd /path/to/chat_pdf

# Step 2 — deactivate the current venv if active
deactivate

# Step 3 — delete the broken venv
rm -rf .venv

# Step 4 — recreate the venv
python3 -m venv .venv

# Step 5 — activate the new venv
source .venv/bin/activate

# Step 6 — install dependencies
pip install -r requirements.txt
```

---

## 8. Troubleshooting — Common Problems

| Problem | Solution |
|---|---|
| `Configuration error` / `api_key field required` | Create `conf/env/.env.local` containing `api_key=sk-...` |
| `Could not load PDF` | File may be corrupt, password-protected, or not a valid PDF |
| `Could not get a response` | Check your internet connection and that your API key is valid |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside your virtual environment |
| `No module named desktop_local` | Run from the project root using `python -m desktop_local.main` |
| App window does not appear | Ensure PyQt6 installed correctly for your OS |