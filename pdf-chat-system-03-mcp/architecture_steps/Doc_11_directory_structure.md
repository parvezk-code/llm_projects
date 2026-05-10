# Directory Structure
> Note: the codebase now uses the word `services` instead of `domain`.

```


root(chat pdf app)/
│
├── main.py                              # Entry point — creates QApplication, MainWindow, 
│                                          MainController
├── requirements.txt
├── __init__.py
│
├── app/
│   ├── __init__.py
│   ├── main_controller.py                # MainController:  orchestrates all event flows
│   │
│   ├── event_handlers/
│   │   ├── __init__.py
│   │   ├── pdf/
│   │   │   ├── __init__.py
│   │   │   ├── upload_pdf_handler.py     # Full PDF upload flow
│   │   │   └── remove_pdf_handler.py     # PDF removal
│   │   │
│   │   ├── chat/
│   │   │   ├── __init__.py
│   │   │   ├── send_message_handler.py   # Single chat with llm 
│   │   │   └── clear_chat_handler.py     # Clear all chats
│   │   │
│   │   └── ui/
│   │       ├── __init__.py
│   │       └── theme_changed_handler.py  # Stub — receives theme_name, will apply it
│   │
│   └── models/
│       ├── __init__.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── pdf_document.py                 # PDFDocument dataclass
│       │   │
│       │   └── llm_transaction/
│       │       └── chat_message.py           # ChatMessage
│       │
│       └── state/
│            ├── __init__.py
│            ├── app_state.py              # AppState dataclass
│            ├── app_state_store.py        # future/planned only. app is without store.
│            └── app_error.py              # future/planned only. app is without AppError
│   
├── ui/
│   ├── __init__.py
│   ├── ui_composer.py                   # UIComposer — builds all UI, returns UIBundle
│   ├── ui_bundle.py                     # UIBundle frozen dataclass
│   │
│   ├── toolbar/
│   │   ├── __init__.py
│   │   ├── toolbar_component.py         # ToolbarComponent 
│   │   ├── toolbar_controller.py        # ToolbarController
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── upload_button_widget.py
│   │       ├── filename_label_widget.py
│   │       ├── clear_button_widget.py
│   │       └── theme_combo_widget.py
│   │
│   ├── file_picker/
│   │   ├── __init__.py
│   │   ├── file_picker.py                   # FilePickerComponent  
│   │   └── file_picker_controller.py        # FilePickerController
│   │
│   ├── status_bar/
│   │   ├── __init__.py
│   │   ├── status_bar_component.py      # StatusBarComponent 
│   │   └── status_bar_controller.py     # StatusBarController
│   │
│   ├── chat_area/
│   │   ├── __init__.py
│   │   ├── chat_area_component.py       # ChatAreaComponent 
│   │   ├── chat_area_controller.py      # ChatAreaController
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── message_bubble_widget.py # MessageBubbleWidget
│   │       └── placeholder_widget.py    # PlaceholderWidget 
│   │
│   └── input_bar/
│       ├── __init__.py
│       ├── input_bar_component.py       # InputBarComponent 
│       ├── input_bar_controller.py      # InputBarController
│       └── widgets/
│           ├── __init__.py
│           ├── button_widget.py 
│           └── text_input_widget.py
│
├── services/
│   ├── __init__.py
│   ├── service_composer.py              # ServiceComposer — instantiates controllers and 
│   │                                      services, config, returns ServiceBundle
│   ├── service_bundle.py                # ServiceBundle frozen dataclass
│   │                                      holds PDFController, LLMController
│   ├── pdf/
│   │   ├── __init__.py
│   │   ├── pdf_controller.py            # PDFController — receives file path, 
│   │   │                                  calls PDFService, returns PDFDocument
│   │   └── pdf_service.py               # PDFService — raw PyMuPDF text extraction, 
│   │                                      simple types only
│   │  
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── llm_controller.py            # LLMController — receives LLMRequest,  
│   │   │                                  calls LLMService, returns LLMResponse
│   │   ├── llm_service.py               # LLMService: raw OpenAI API call, simple types only
│   │   ├── request.py                   # LLMRequest: send to llm controller by main controller
│   │   ├── response.py                  # LLMResponse: returned by llm controller to main controller
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── openai_formatter.py       # OpenAIFormatter class
│   │
│   └── mcp/
│       ├── __init__.py
│       ├── tool_registry.py              # MCPToolRegistry(returns list of tools)
|       |
│       ├── clients/
│       |   ├── __init__.py
│       |   ├── client_async.py           # classes: MCPConnectionClient
│       |   └── client_sync.py            # classes: SyncConnection
|       |
|       ├── controller.py                 # MCPToolController
│       ├── models/
│       │   ├── __init__.py
│       │   └── mcp_tool_definition.py    # classes : ToolParameter, ToolDefinition 
|       |
│       └── tools_json/
│           ├── tool_get_directory.json   # tool definition : get working directory path
│           ├── tool_list_pdfs.json       # tool definition : get list of pdfs in dir
│           └── tool_read_pdf             # tool definition : get content of pdf
│
├── conf/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── appConfig.py                  # shared/global config
│   │   ├── openAI.py                     # LLM-specific
│   │   ├── mcp.py                        # MCP-specific
│   │   └── config_bundle.py              # aggregates all settings
│   │
│   └── env/                              # NO __init__.py — contains only .env files
│       ├── .env.app                      # shared/global config 
│       ├── .env.openAI.example           # example of file .env.openAI
│       ├── .env.openAI                   # LLM-specific
│       └── .env.mcp                      # MCP Server
│
├── styles/                               # NO __init__.py — contains only .qss files
│
└── utils/ 
      └── __init__.py


```

---

## File Responsibilities

| File | Contains |
|---|---|
| `main.py` | App entry point. Creates `QApplication`, `MainWindow`, instantiates `MainController` |
| `app/main_controller.py` | Slim orchestrator. Builds UI, services, and state. Instantiates all event handlers. Wires signals to handler methods via `_bind_signals`. Owns `AppState`. |
| `app/event_handlers/pdf/upload_pdf_handler.py` | Handles the full PDF upload flow. Opens the file picker on upload click, calls `PDFService` via `PDFController`, updates `AppState`, refreshes toolbar, chat area, and input bar. Handles `PDFLoadError` and surfaces it to the status bar. |
| `app/event_handlers/pdf/remove_pdf_handler.py` | Handles PDF removal. Clears `state.pdf`, resets message history and error, empties the chat area, and disables input. |
| `app/event_handlers/chat/send_message_handler.py` | Handles a single chat turn. Builds an `LLMTransaction` from current state, calls `LLMController`, appends both the user message and the LLM response to `AppState`, and updates the chat area and toolbar. Handles `LLMCallError` and surfaces it to the status bar. |
| `app/event_handlers/chat/clear_chat_handler.py` | Handles chat clear. Resets message history and error in `AppState`, empties the chat area, hides the status bar, and disables input. |
| `app/event_handlers/ui/theme_changed_handler.py` | Stub handler for theme switching. Receives a `theme_name` string and will apply it to the app stylesheet when implemented. |
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
| `conf/settings/config_bundle.py` | Buldles objects into AppSettings. These objects expose .env files inside conf/env directory|
| `conf/settings/appConfig.py` | Defines `AppConfig` settings loaded from `conf/env/.env.app` |
| `conf/env/.env.openAI` | Environment values for OpenAI settings used by `OpenAIConfig` |
| `conf/env/.env.openAI.example` | Example OpenAI environment file template |
| `utils/` | future/planned only. Shared helpers. Empty for now |


## Models
  - Use Pydantic only at boundaries where data comes from outside. Use dataclass for internal app models.
  - Use Pydantic if data comes from: JSON files, .env/config validation, external request/response formats
