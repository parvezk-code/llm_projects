# Directory Structure
> Note : the name domain is being replaced with services

```
chat_pdf/
│
├── main.py                              # Entry point — creates QApplication, MainWindow, 
│                                          MainController
├── .env                                 # API key (not committed to version control)
├── requirements.txt
│
├── app/
│   ├── main_controller.py               # MainController — orchestrates all event flows
│   └── models/
│       ├── services/
│       │   ├── pdf_document.py          # PDFDocument dataclass
│       │   ├── llm_transaction.py        # LLMTransaction dataclass
│       │   └── chat_message.py          # ChatMessage dataclass
│       └── state/
│           ├── app_state.py             # AppState dataclass
│           └── app_error.py             # This file not needed (AppError dataclass)
│
├── ui/
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns UIBundle
│   ├── ui_bundle.py                     # UIBundle frozen dataclass
│   ├── toolbar/
│   │   ├── toolbar_component.py         # ToolbarComponent [SMART]
│   │   └── toolbar_controller.py        # ToolbarController
│   │   └── widgets/
│   │       ├── upload_button_widget.py
│   │       ├── filename_label_widget.py
│   │       ├── clear_button_widget.py
│   │       └── theme_combo_widget.py
│   │
│   ├── status_bar/
│   │   ├── status_bar_component.py      # StatusBarComponent [SMART]
│   │   └── status_bar_controller.py     # StatusBarController
│   ├── chat_area/
│   │   ├── chat_area_component.py       # ChatAreaComponent [SMART]
│   │   ├── chat_area_controller.py      # ChatAreaController
│   │   └── widgets/
│   │       ├── message_bubble_widget.py # MessageBubbleWidget [DUMB]
│   │       ├── loading_bubble_widget.py # LoadingBubbleWidget [DUMB]
│   │       └── placeholder_widget.py   # PlaceholderWidget [DUMB]
│   └── input_bar/
│       ├── input_bar_component.py       # InputBarComponent [SMART]
│       ├── input_bar_controller.py      # InputBarController
│       └── widgets/
│           ├── button_widget.py 
│           └── text_input_widget.py
│
├── services/
│   ├── service_composer.py              # ServiceComposer — instantiates controllers and 
│   │                                      services, returns ServiceBundle
│   ├── service_bundle.py                # ServiceBundle frozen dataclass
│   │                                      holds PDFController, LLMController
│   ├── pdf/
│   │   ├── pdf_controller.py            # PDFController — receives file path, 
│   │   |                                  calls PDFService, returns PDFDocument
│   │   └── pdf_service.py               # PDFService — raw PyMuPDF text extraction, 
│   │                                      simple types only
│   │  
│   └── llm/
│       ├── llm_controller.py            # LLMController — receives LLMTransaction,  
│       |                                  calls LLMService, returns LLMTransaction
│       └── llm_service.py               # LLMService: raw OpenAI API call, simple types only
│
│
├── config/
│   ├── settings/
│   │   ├── appConfig.py                  # shared/global config
│   │   ├── openAI.py                     # LLM-specific
│   │   └── settings.py                   # aggregates all settings
│   │
│   └── env/
│       ├── .env.app                      # shared/global config
│       └── .env.openAI                   # LLM-specific
│
│
└── utils/                               # Shared helpers (empty for now)

```

---

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | App entry point. Creates `QApplication`, `MainWindow`, instantiates `MainController` |
| `app/main_controller.py` | All event handlers, signal wiring, `AppState` ownership |
| `app/models/services/pdf_document.py` | `PDFDocument` dataclass |
| `app/models/services/chat_message.py` | `ChatMessage` dataclass |
| `app/models/services/llm_transaction.py` | `LLMTransaction` dataclass |
| `app/models/state/app_state.py` | `AppState` dataclass |
| `app/models/state/app_error.py` | `AppError` dataclass, `ErrorKind` enum |
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to all component controllers |
| `ui/ui_composer.py` | Builds all components + controllers, returns `UIBundle` |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Upload button, filename label, Clear button |
| `ui/toolbar/toolbar_controller.py` | File picker, filename display, Clear button state |
| `ui/status_bar/status_bar_component.py` | Error banner UI — icon, message label, dismiss button |
| `ui/status_bar/status_bar_controller.py` | Show/hide error banner |
| `ui/chat_area/chat_area_component.py` | Scrollable chat area UI — bubble container |
| `ui/chat_area/chat_area_controller.py` | Bubble management, scroll, placeholder, loading indicator |
| `ui/chat_area/widgets/message_bubble_widget.py` | Single message bubble [DUMB] |
| `ui/chat_area/widgets/loading_bubble_widget.py` | Animated `• • •` loading bubble [DUMB] |
| `ui/chat_area/widgets/placeholder_widget.py` | Empty state icon + hint text [DUMB] |
| `ui/input_bar/input_bar_component.py` | Input field + Send button UI |
| `ui/input_bar/input_bar_controller.py` | Read input, clear input, enable/disable |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds refs to `PDFController`, `LLMController` |
| `services/service_composer.py` | Instantiates all controllers and services, returns `ServiceBundle` |
| `services/pdf/pdf_controller.py` | `PDFController` — receives file path, calls `PDFService`, returns `PDFDocument` |
| `services/pdf/pdf_service.py` | `PDFService` — raw PyMuPDF text extraction, simple types only |
| `services/llm/llm_controller.py` | `LLMController` — receives `LLMTransaction`, calls `LLMService`, returns `str` |
| `services/llm/llm_service.py` | `LLMService` — raw OpenAI API call, simple types only |
| `config/settings.py` | Loads `.env` via python-dotenv, exposes `OPENAI_API_KEY` constant |
| `utils/` | Shared helpers — empty for now |


## Models
  - Use Pydantic only at boundaries where data comes from outside. Use dataclass for internal app models.
  - Use Pydantic if data comes from: JSON files, .env/config validation, external request/response formats