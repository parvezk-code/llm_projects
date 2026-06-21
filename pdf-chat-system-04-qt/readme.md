# Chat PDF App — Setup & Run Guide

---

## Prerequisites

- Python 3.11 or higher
- An OpenAI API key

---

## 1. Clone or Download the Project

```bash
cd chat_pdf
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
python main.py
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

---

## 7. Project Structure

```
chat_pdf/
├── main.py
├── .env
├── requirements.txt
├── app/
│   ├── main_controller.py
│   └── models/
│       ├── services/
│       │   ├── pdf_document.py
│       │   ├── chat_message.py
│       │   └── llm_transaction.py
│       └── state/
│           └── app_state.py
├── ui/
│   ├── ui_composer.py
│   ├── ui_bundle.py
│   ├── toolbar/
│   │   ├── toolbar_component.py
│   │   └── toolbar_controller.py
│   ├── status_bar/
│   │   ├── status_bar_component.py
│   │   └── status_bar_controller.py
│   ├── chat_area/
│   │   ├── chat_area_component.py
│   │   ├── chat_area_controller.py
│   │   └── widgets/
│   │       ├── message_bubble_widget.py
│   │       ├── loading_bubble_widget.py
│   │       └── placeholder_widget.py
│   └── input_bar/
│       ├── input_bar_component.py
│       └── input_bar_controller.py
├── services/
│   ├── service_bundle.py
│   ├── service_composer.py
│   ├── pdf/
│   │   ├── pdf_controller.py
│   │   └── pdf_service.py
│   └── llm/
│       ├── llm_controller.py
│       └── llm_service.py
└── config/
    └── settings.py
```

---

## 8. Troubleshooting

| Problem | Solution |
|---|---|
| `OPENAI_API_KEY not found` | Check your `.env` file exists and contains the key |
| `Failed to load PDF` | File may be corrupt, password-protected, or not a valid PDF |
| `Could not reach OpenAI API` | Check your internet connection and API key validity |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside your virtual environment |
| App window does not appear | Ensure PyQt6 is installed correctly for your OS |
