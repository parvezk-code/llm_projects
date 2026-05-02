# Directory Structure
> Note: the codebase now uses the word `services` instead of `domain`.

```
root(chat pdf app)/
│
├── main.py                              # Entry point — creates QApplication, MainWindow, 
│                                          MainController
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
│           ├── app_state_store.py       # future/planned only. Currently app is without store.
│           └── app_error.py             # future/planned only. This file not needed (AppError dataclass)
│
├── ui/
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns UIBundle
│   ├── ui_bundle.py                     # UIBundle frozen dataclass
│   │
│   ├── toolbar/
│   │   ├── toolbar_component.py         # ToolbarComponent 
│   │   └── toolbar_controller.py        # ToolbarController
│   │   └── widgets/
│   │       ├── upload_button_widget.py
│   │       ├── filename_label_widget.py
│   │       ├── clear_button_widget.py
│   │       └── theme_combo_widget.py
│   │
│   ├── file_picker/
│   │   ├── file_picker.py                   # FilePickerComponent  
│   │   └── file_picker_controller.py        # FilePickerController
│   │
│   ├── status_bar/
│   │   ├── status_bar_component.py      # StatusBarComponent 
│   │   └── status_bar_controller.py     # StatusBarController
│   │
│   ├── chat_area/
│   │   ├── chat_area_component.py       # ChatAreaComponent 
│   │   ├── chat_area_controller.py      # ChatAreaController
│   │   └── widgets/
│   │       ├── message_bubble_widget.py # MessageBubbleWidget
│   │       └── placeholder_widget.py    # PlaceholderWidget 
│   │
│   └── input_bar/
│       ├── input_bar_component.py       # InputBarComponent 
│       ├── input_bar_controller.py      # InputBarController
│       └── widgets/
│           ├── button_widget.py 
│           └── text_input_widget.py
│
├── services/
│   ├── service_composer.py              # ServiceComposer — instantiates controllers and 
│   │                                      services, config, returns ServiceBundle
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
├── conf/
│   ├── settings/
│   │   ├── appConfig.py                  # shared/global config
│   │   ├── openAI.py                     # LLM-specific
│   │   └── settings.py                   # aggregates all settings
│   │
│   └── env/
│       ├── .env.app                      # shared/global config 
│       ├── .env.openAI.example           # example of file .env.openAI
│       └── .env.openAI                   # LLM-specific
│
│
├── styles/                               # contains qss files to style the PyQt6 widgets
│
└── utils/                                # Shared helpers (empty for now)

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
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to all component controllers |
| `ui/ui_composer.py` | Builds all components + controllers, returns `UIBundle` |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Upload button, filename label, Clear button |
| `ui/toolbar/toolbar_controller.py` | filename display, Clear button state, signal binding |
| `ui/file_picker/file_picker_controller.py` | Opens PDF picker dialog |
| `ui/status_bar/status_bar_component.py` | Error banner UI — icon, message label, dismiss button |
| `ui/status_bar/status_bar_controller.py` | Show/hide error banner |
| `ui/chat_area/chat_area_component.py` | Scrollable chat area UI — bubble container |
| `ui/chat_area/chat_area_controller.py` | Bubble management, scroll, placeholder |
| `ui/chat_area/widgets/message_bubble_widget.py` | Single message bubble  |
| `ui/chat_area/widgets/placeholder_widget.py` | Empty state icon + hint text  |
| `ui/input_bar/input_bar_component.py` | Input field + Send button UI |
| `ui/input_bar/input_bar_controller.py` | Read input, clear input, enable/disable |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds refs to `PDFController`, `LLMController` |
| `services/service_composer.py` | Instantiates all controllers and services, returns `ServiceBundle` |
| `services/pdf/pdf_controller.py` | `PDFController` — receives file path, calls `PDFService`, returns `PDFDocument` |
| `services/pdf/pdf_service.py` | `PDFService` — raw PyMuPDF text extraction, simple types only |
| `services/llm/llm_controller.py` | `LLMController` — receives `LLMTransaction`, calls `LLMService`, returns `LLMTransaction` |
| `services/llm/llm_service.py` | `LLMService` — raw OpenAI API call, simple types only |
| `conf/env/.env.app` | Environment values for shared app settings used by `AppConfig` |
| `conf/settings/openAI.py` | Defines `OpenAIConfig` settings loaded from `conf/env/.env.openAI` and `conf/env/.env.local` |
| `conf/settings/settings.py` | Buldles objects into AppSettings. These objects expose .env files inside conf/env directory|
| `conf/settings/appConfig.py` | Defines `AppConfig` settings loaded from `conf/env/.env.app` |
| `conf/env/.env.openAI` | Environment values for OpenAI settings used by `OpenAIConfig` |
| `conf/env/.env.openAI.example` | Example OpenAI environment file template |
| `utils/` | future/planned only. Shared helpers. Empty for now |


## Models
  - Use Pydantic only at boundaries where data comes from outside. Use dataclass for internal app models.
  - Use Pydantic if data comes from: JSON files, .env/config validation, external request/response formats