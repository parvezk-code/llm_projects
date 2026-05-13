# Coding Agent — Level 1 Directory Structure
> LangChain Basics: ChatOpenAI + ChatPromptTemplate + LCEL Chain + PyQt6 UI

---

## What Level 1 Covers

- `ChatOpenAI` — LangChain's OpenAI LLM wrapper
- `ChatPromptTemplate` — system + human message templates
- LCEL chain — `prompt | llm | output_parser` pipe operator
- `StrOutputParser` — parses LLM output to plain string
- PyQt6 UI — chat interface wired to the LangChain chain
- Threading — `QThread` worker so the UI never freezes

No tools. No RAG. No agents. Just clean LangChain chain → PyQt6 wiring.

---

## Directory Structure

```
coding-agent/
├── __init__.py
├── main.py
├── requirements.txt
│
├── app/
├── ui/
├── services/
├── conf/
├── storage/
├── styles/    --->  main.qss
└── utils/     --->  __init__.py, logger.py

```

```

app/
├── __init__.py
├── main_controller.py
│
├── state/
│   ├── __init__.py
│   ├── app_state.py
│   ├── state_controller.py
│   └── models/
│       ├── __init__.py
│       └── chat_message.py
│
└── event_handlers/
    ├── __init__.py
    ├── transformers/
    │   ├── __init__.py
    │   └── chain/
    │       ├── __init__.py
    │       └── history_transformer.py
    ├── business_logic/
    │   ├── __init__.py
    │   └── project/
    │       ├── __init__.py
    │       └── retriever_pipeline_worker.py
    ├── chat/
    │   ├── __init__.py
    │   ├── send_message_handler.py
    │   └── clear_chat_handler.py
    └── project/
        ├── __init__.py
        └── load_project_handler.py

```

```

services/
├── __init__.py
├── service_composer.py
├── service_bundle.py
│
├── chain/
│   ├── __init__.py
│   ├── chain_controller.py
│   ├── chain_service.py
│   ├── request.py
│   ├── response.py
│   └── worker.py
│
├── retriever/
│   ├── __init__.py
│   └── pipeline/
│       ├── __init__.py
│       ├── controller.py
│       ├── service.py
│       ├── request.py
│       └── response.py
│
├── document_extractors/
│   ├── __init__.py
│   └── text/
│       ├── __init__.py
│       └── plain/
│           ├── __init__.py
│           ├── controller.py
│           ├── service.py
│           ├── request.py
│           └── response.py
│
├── chunking/
│   ├── __init__.py
│   └── code/
│       ├── __init__.py
│       ├── controller.py
│       ├── service.py
│       ├── request.py
│       └── response.py
│
├── embedding_generators/
│   ├── __init__.py
│   └── openai/
│       ├── __init__.py
│       ├── controller.py
│       ├── service.py
│       ├── request.py
│       └── response.py
│
└── vector_stores/
    ├── __init__.py
    └── faiss/
        ├── __init__.py
        ├── controller.py
        ├── service.py
        ├── request.py
        └── response.py

```


```
coding-agent/ui/
├── __init__.py
├── ui_composer.py
├── ui_bundle.py
│
├── toolbar/
│   ├── __init__.py
│   ├── toolbar_component.py
│   ├── toolbar_controller.py
│   └── widgets/
│       ├── __init__.py
│       ├── clear_button_widget.py
│       ├── load_project_button_widget.py
│       └── project_label_widget.py
│
├── status_bar/
│   ├── __init__.py
│   ├── status_bar_component.py
│   └── status_bar_controller.py
│
├── chat_area/
│   ├── __init__.py
│   ├── chat_area_component.py
│   ├── chat_area_controller.py
│   └── widgets/
│       ├── __init__.py
│       ├── message_bubble_widget.py
│       └── placeholder_widget.py
│
└── input_bar/
    ├── __init__.py
    ├── input_bar_component.py
    ├── input_bar_controller.py
    └── widgets/
        ├── __init__.py
        ├── send_button_widget.py
        └── text_input_widget.py

```

```

coding-agent/conf/
├── __init__.py
│
├── settings/
│   ├── __init__.py
│   ├── app_config.py
│   ├── openai_config.py
│   ├── retriever_config.py
│   └── config_bundle.py
│
└── env/
    ├── .env.app
    ├── .env.openai
    ├── .env.openai.example
    ├── .env.retriever
    └── .env.retriever.example


```

---


Here are the updated file responsibility tables:

---

## File Responsibilities — Entry Point + App Layer

| File | Contains |
|---|---|
| `main.py` | Entry point. Calls `configure_logging()`. Creates `QApplication`, `MainWindow`. Instantiates `MainController`. |
| `utils/logger.py` | `configure_logging()` — configures Python logging to stdout with timestamp and level prefix. Called once at startup. |
| `app/main_controller.py` | Slim orchestrator. Builds UI via `UIComposer`, services via `ServiceComposer`. Owns `AppState` and `StateController`. Instantiates all event handlers. Wires signals to handler methods via `_bind_signals()`. |
| `app/event_handlers/chat/send_message_handler.py` | Handles a single chat turn. Reads user input. Reads history via `StateController`. Calls `history_transformer` to convert history. Builds `ChainRequest`. Starts `ChainWorker` (QThread). On result: saves messages via `StateController`, appends bubbles to chat area, re-enables input. On error: shows status bar, rolls back user message. |
| `app/event_handlers/chat/clear_chat_handler.py` | Clears history and error via `StateController`. Empties chat area. Hides status bar. Disables input bar. |

---

## File Responsibilities — App State

| File | Contains |
|---|---|
| `app/state/models/chat_message.py` | `ChatMessage` dataclass — `role: str` and `content: str`. Internal model. Not Pydantic. |
| `app/state/app_state.py` | `AppState` dataclass — `messages: list[ChatMessage]`, `error: str | None`. |
| `app/state/state_controller.py` | `StateController` — owns all reads and writes to `AppState`. Exposes `add_message()`, `get_messages()`, `pop_last_message()`, `clear_history()`, `has_messages()`, `set_error()`, `clear_error()`, `get_error()`. |

---

## File Responsibilities — Event Handler Transformers

| File | Contains |
|---|---|
| `app/event_handlers/transformers/chain/history_transformer.py` | `convert_history(messages: list[ChatMessage]) → list[BaseMessage]`. Pure function. Converts internal `ChatMessage` dataclasses to LangChain `HumanMessage` / `AIMessage` types. Called by `SendMessageHandler` before building `ChainRequest`. |

---

## File Responsibilities — UI Layer

| File | Contains |
|---|---|
| `ui/ui_composer.py` | `UIComposer` — builds all components and controllers. Returns `UIBundle`. |
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to `ToolbarController`, `ChatAreaController`, `InputBarController`, `StatusBarController`. |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Clear button only at Level 1. |
| `ui/toolbar/toolbar_controller.py` | Enable/disable Clear button. Exposes `clear_clicked` signal. |
| `ui/toolbar/widgets/clear_button_widget.py` | Clear chat QPushButton widget. |
| `ui/status_bar/status_bar_component.py` | Error banner — icon, message label, dismiss button. Hidden by default. |
| `ui/status_bar/status_bar_controller.py` | `show_error(msg)` and `hide()` methods. |
| `ui/chat_area/chat_area_component.py` | Scrollable bubble container. |
| `ui/chat_area/chat_area_controller.py` | `add_bubble(role, content)`, `clear()`, `scroll_to_bottom()`, placeholder toggle. |
| `ui/chat_area/widgets/message_bubble_widget.py` | Single message bubble. Styled differently for `user` vs `assistant` role. |
| `ui/chat_area/widgets/placeholder_widget.py` | Empty state widget — icon and hint text. Shown when `messages` is empty. |
| `ui/input_bar/input_bar_component.py` | Text input + Send button UI. |
| `ui/input_bar/input_bar_controller.py` | `get_text()`, `clear_text()`, `set_enabled(bool)`. Exposes `send_clicked` signal. |
| `ui/input_bar/widgets/send_button_widget.py` | Send QPushButton widget. |
| `ui/input_bar/widgets/text_input_widget.py` | QTextEdit input widget. Emits submit on Ctrl+Enter. |

---

## File Responsibilities — Services — Chain

| File | Contains |
|---|---|
| `services/chain/chain_controller.py` | `ChainController` — receives `ChainRequest`. Calls `ChainService.run()`. Returns `ChainResponse`. No conversion logic — history arrives already formatted as `list[BaseMessage]`. |
| `services/chain/chain_service.py` | `ChainService` — owns the LCEL chain: `prompt | llm | output_parser`. `ChatPromptTemplate` holds system prompt + message placeholder. `ChatOpenAI` is configured from `OpenAIConfig`. `StrOutputParser` returns plain string. Accepts formatted message list. Returns raw string. |
| `services/chain/request.py` | `ChainRequest` Pydantic model — `system_prompt: str`, `history: list[BaseMessage]`, `user_input: str`. Pydantic because it crosses the service boundary. |
| `services/chain/response.py` | `ChainResponse` Pydantic model — `answer: str | None`, `error: str | None`. Methods: `has_answer()`, `has_error()`. |
| `services/chain/worker.py` | `ChainWorker(QThread)` — calls `ChainController.run(request)` in background thread. Emits `result_ready = pyqtSignal(str)` and `error_occurred = pyqtSignal(str)`. |

---

## File Responsibilities — Services — Wiring

| File | Contains |
|---|---|
| `services/service_composer.py` | `ServiceComposer` — reads `ConfigBundle`. Instantiates `ChainService(openai_config)` and `ChainController(chain_service)`. Returns `ServiceBundle`. |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds `chain_controller: ChainController`. |

---

## File Responsibilities — Configuration

| File | Contains |
|---|---|
| `conf/settings/app_config.py` | `AppConfig` — Pydantic BaseSettings from `.env.app`. Fields: `app_name: str`, `system_prompt: str`. |
| `conf/settings/openai_config.py` | `OpenAIConfig` — Pydantic BaseSettings from `.env.openai`. Fields: `api_key: str`, `model: str`, `temperature: float`, `max_tokens: int`. |
| `conf/settings/config_bundle.py` | `ConfigBundle` dataclass — holds `app: AppConfig`, `openai: OpenAIConfig`. Instantiated once in `main.py`, passed to `ServiceComposer` and `UIComposer`. |
| `conf/env/.env.app` | `APP_NAME`, `SYSTEM_PROMPT` |
| `conf/env/.env.openai` | `OPENAI_API_KEY`, `OPENAI_MODEL`, `TEMPERATURE`, `MAX_TOKENS` |
| `conf/env/.env.openai.example` | Safe-to-commit template. API key value is empty. |

---

## Key LangChain Concepts Introduced at Level 1

| Concept | Where It Lives | What You Learn |
|---|---|---|
| `ChatOpenAI` | `chain_service.py` | How LangChain wraps the OpenAI API |
| `ChatPromptTemplate` | `chain_service.py` | How to define system + human message templates |
| `MessagesPlaceholder` | `chain_service.py` | How to inject chat history into the prompt |
| LCEL `|` operator | `chain_service.py` | How to chain prompt → llm → parser |
| `StrOutputParser` | `chain_service.py` | How to extract plain text from LLM response |
| `HumanMessage` / `AIMessage` | `history_transformer.py` | How LangChain represents conversation history |

---

## What Changes at Level 2 (RAG)

At Level 2, the following are added without changing anything above:

- `services/retriever/` — document loader, text splitter, vector store, retriever
- `services/chain/chain_service.py` — swaps plain chain for `create_retrieval_chain()`
- `ui/toolbar/` — gains a folder picker widget to load a codebase
- `app/state/app_state.py` — gains `project_path: str | None`

---

## Models Convention

> Use **Pydantic** only at service boundaries (data crossing in/out of a service layer).
> Use **dataclass** for all internal app models (`AppState`, `ChatMessage`).