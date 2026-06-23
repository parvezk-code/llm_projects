# Chat PDF App — Setup & Run Guide

---

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key

---

## 1. Clone or Download the Project

```bash
cd root_coding_agent
```

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
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create the `.env` File

In the root of the project (`chat_pdf/`), create a file named `.env`:

```
OPENAI_API_KEY=sk-your-api-key-here

OPENAI_MODEL=gpt-4o-mini

```

> ⚠️ Never commit this file to version control. It is already excluded if you have a `.gitignore`.

---

## 5. Run the App

```bash

python -m desktop_local.main

```

---



## Troubleshooting — If `pip install` Fails

If `pip install -r requirements.txt` fails or pip stops working after a previously successful install, the virtual environment is likely corrupted. Recreate it from scratch by running these commands from the project root:

```bash
# Step 1 — navigate to the project root
cd /path/to/pdf_chat

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

---

## 7. Troubleshooting

| Problem | Solution |
|---|---|
| `OPENAI_API_KEY not found` | Check your `.env` file exists and contains the key |
| `Failed to load PDF` | File may be corrupt, password-protected, or not a valid PDF |
| `Could not reach OpenAI API` | Check your internet connection and API key validity |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside your virtual environment |
| App window does not appear | Ensure PyQt6 is installed correctly for your OS |
