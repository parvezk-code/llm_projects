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
├── styles/    --->  main.qss
└── utils/     --->  __init__.py, logger.py

```

```

coding-agent/app/
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
├── applications/
│   ├── __init__.py
│   ├── application_bundle.py
│   ├── send_message_command.py
│   ├── clear_chat_command.py
│   └── load_project_command.py
|
├── utils/
│   ├── __init__.py
│   └── worker.py
│
└── event_handlers/
    ├── __init__.py
    ├── transformers/
    │   ├── __init__.py
    │   └── chain/
    │       ├── __init__.py
    │       └── history_transformer.py
    ├── chat/
    │   ├── __init__.py
    │   ├── send_message_handler.py
    │   └── clear_chat_handler.py
    └── project/
        ├── __init__.py
        └── load_project_handler.py

```

```

coding-agent/services/
├── __init__.py
├── service_composer.py
├── service_bundle.py
│
├── chain/
│   ├── __init__.py
│   ├── chain_controller.py
│   ├── request.py
│   ├── response.py
│   ├── plain/
│   │   ├── __init__.py
│   │   └── plain_chain_service.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── retrieval_chain_service.py
│   └── agent/
│       ├── __init__.py
│       └── agent_chain_service.py
│
├── tools/
│   ├── __init__.py
│   ├── run_code/
│   │   ├── __init__.py
│   │   ├── executor.py
│   │   └── tool.py
│   ├── read_file/
│   │   ├── __init__.py
│   │   └── tool.py
│   ├── write_file/
│   │   ├── __init__.py
│   │   └── tool.py
│   └── list_directory/
│       ├── __init__.py
│       └── tool.py
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
├── folder_picker/
│   ├── __init__.py
│   ├── folder_picker_component.py
│   └── folder_picker_controller.py
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
| `main.py` | Entry point. Calls `configure_logging()`. Creates `QApplication`, `MainWindow`. Loads config via `load_config()`. Instantiates `MainController`. |
| `utils/logger.py` | `configure_logging()` — configures Python logging to stdout with timestamp and level prefix. Called once at startup. |
| `app/main_controller.py` | Slim orchestrator. Builds UI via `UIComposer`, services via `ServiceComposer`. Owns `AppState` and `StateController`. Instantiates `ApplicationBundle` and all event handlers. Wires signals to handler methods via `_bind_signals()` using `bind_*` methods on controllers. Wires `mode_changed` signal to `state.set_mode()`. |
| `app/event_handlers/chat/send_message_handler.py` | UI-only handler. Reads user input via `UIBundle`. Adds user bubble to chat area. Starts `Worker` (QThread) with `SendMessageCommand.execute()`. On result: appends assistant bubble — on error: removes user bubble, shows status bar. Delegates all business logic to `ApplicationBundle.send_message`. |
| `app/event_handlers/chat/clear_chat_handler.py` | UI-only handler. Delegates state reset to `ApplicationBundle.clear_chat`. Then clears chat area, hides status bar, resets toolbar project label, re-enables input. |
| `app/event_handlers/project/load_project_handler.py` | UI-only handler. Disables UI. Starts `Worker` with `LoadProjectCommand.execute()`. On success: calls `send_message.set_retriever()`, updates toolbar project label, re-enables UI. On error: shows status bar error, re-enables UI. Delegates all business logic to `ApplicationBundle.load_project`. |
| `app/event_handlers/utils/worker.py` | Generic `Worker(QThread)` — accepts any callable `method` and `on_result` callback. Calls `method()` in background thread. Emits `result_ready` signal with full response object. Handler is responsible for checking `response.has_error()`. |

---

## File Responsibilities — Applications Layer

| File | Contains |
|---|---|
| `app/applications/send_message_command.py` | Pure business logic for a chat turn. Adds user message to state. Converts history via `history_transformer`. Builds `ChainRequest` with `mode`, `retriever`, and `project_path` from state. Calls `chain_controller.run()`. On success adds assistant message to state — on error rolls back user message. Returns `ChainResponse`. No Qt. Owns `_retriever` — set externally via `set_retriever()` when RAG mode is active. |
| `app/applications/clear_chat_command.py` | Clears history, error, and project path in state via `StateController`. No Qt. |
| `app/applications/load_project_command.py` | Orchestrates extraction → chunking → vector store build in sequence. Calls `extractor_controller`, `chunking_controller`, `vector_store_controller` from `ServiceBundle`. On success sets project path in state. Returns the vector store response. No Qt. |
| `app/applications/application_bundle.py` | `ApplicationBundle` frozen dataclass — holds `send_message: SendMessageCommand`, `clear_chat: ClearChatCommand`, `load_project: LoadProjectCommand`. |

---

## File Responsibilities — App State

| File | Contains |
|---|---|
| `app/state/models/chat_message.py` | `ChatMessage` dataclass — `role: str` and `content: str`. Internal model. Not Pydantic. |
| `app/state/app_state.py` | `AppState` dataclass — `messages: list[ChatMessage]`, `error: str | None`, `project_path: str | None`, `mode: str = "Simple"`. |
| `app/state/state_controller.py` | `StateController` — owns all reads and writes to `AppState`. Exposes `add_message()`, `get_messages()`, `pop_last_message()`, `clear_history()`, `has_messages()`, `set_error()`, `clear_error()`, `get_error()`, `set_project_path()`, `get_project_path()`, `has_project()`, `clear_project()`, `set_mode()`, `get_mode()`. |

---

## File Responsibilities — Event Handler Transformers

| File | Contains |
|---|---|
| `app/event_handlers/transformers/chain/history_transformer.py` | `convert_history(messages: list[ChatMessage]) → list[BaseMessage]`. Pure function. Converts internal `ChatMessage` dataclasses to LangChain `HumanMessage` / `AIMessage` types. Called by `SendMessageCommand` before building `ChainRequest`. |

---

## File Responsibilities — UI Layer

| File | Contains |
|---|---|
| `ui/ui_composer.py` | `UIComposer` — builds all components and controllers. Assembles main window layout. Returns `UIBundle`. |
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to `ToolbarController`, `FolderPickerController`, `ChatAreaController`, `InputBarController`, `StatusBarController`. |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Clear button, Load Project button, project label, mode combo. Emits `clear_clicked`, `load_project_clicked`, `mode_changed` signals. Exposes accessors: `set_project_name()`, `clear_project_name()`, `set_enabled()`, `set_clear_enabled()`, `get_mode()`. |
| `ui/toolbar/toolbar_controller.py` | Manages `ToolbarComponent`. Exposes `bind_clear_clicked()`, `bind_load_project_clicked()`, `bind_mode_changed()`. Operation methods: `set_enabled()`, `set_clear_enabled()`, `set_project_name()`, `clear_project_label()`, `get_mode()`. |
| `ui/toolbar/widgets/clear_button_widget.py` | Clear chat QPushButton widget. |
| `ui/toolbar/widgets/load_project_button_widget.py` | Load Project QPushButton widget. |
| `ui/toolbar/widgets/project_label_widget.py` | QLabel showing loaded project folder name. Exposes `set_project_name()` and `clear_project_name()`. |
| `ui/toolbar/widgets/mode_combo_widget.py` | QComboBox with 3 modes: Simple, RAG, Agent. Exposes `get_mode()`. |
| `ui/folder_picker/folder_picker_component.py` | Wraps `QFileDialog` for folder selection. Emits `folder_selected: pyqtSignal(str)` when a folder is chosen. Emits nothing on cancel. Exposes `open()` accessor. |
| `ui/folder_picker/folder_picker_controller.py` | Manages `FolderPickerComponent`. Exposes `bind_folder_selected()` and `open()`. |
| `ui/status_bar/status_bar_component.py` | Error banner — message label, dismiss button. Hidden by default. Emits `dismiss_clicked` signal. Exposes `set_message()`, `clear_message()`. |
| `ui/status_bar/status_bar_controller.py` | Manages `StatusBarComponent`. `show_error(msg)` and `hide()` methods. Exposes `bind_dismiss_clicked()`. |
| `ui/chat_area/chat_area_component.py` | Scrollable bubble container. Exposes `get_container_layout()`, `get_scroll_bar()`, `show_scroll_area()`, `show_placeholder()`. |
| `ui/chat_area/chat_area_controller.py` | `add_bubble(role, content)`, `clear_last_bubble()`, `clear()`. Handles scroll and placeholder toggle. |
| `ui/chat_area/widgets/message_bubble_widget.py` | Single message bubble. Styled differently for `user` vs `assistant` role. |
| `ui/chat_area/widgets/placeholder_widget.py` | Empty state widget — icon and hint text. Shown when `messages` is empty. |
| `ui/input_bar/input_bar_component.py` | Text input + Send button UI. Emits `send_triggered` signal. Exposes `get_text()`, `clear_text()`, `set_enabled()`. Syncs send button enabled state with text content. |
| `ui/input_bar/input_bar_controller.py` | Manages `InputBarComponent`. Exposes `bind_send_clicked()`, `get_text()`, `clear_text()`, `set_enabled()`. Emits `send_clicked` signal. |
| `ui/input_bar/widgets/send_button_widget.py` | Send QPushButton widget. |
| `ui/input_bar/widgets/text_input_widget.py` | QTextEdit input widget. Emits `submit_triggered` on Ctrl+Enter. |

---

## File Responsibilities — Services — Chain

| File | Contains |
|---|---|
| `services/chain/chain_controller.py` | `ChainController` — receives `ChainRequest`. Routes to `PlainChainService`, `RetrievalChainService`, or `AgentChainService` based on `request.mode`. Returns `ChainResponse`. |
| `services/chain/plain/plain_chain_service.py` | `PlainChainService` — owns plain LCEL chain. `prompt | llm | output_parser`. System prompt owned internally. |
| `services/chain/retrieval/retrieval_chain_service.py` | `RetrievalChainService` — owns retrieval LCEL chain. `input_map | prompt | llm | output_parser` using lambda extractors for `context`, `history`, `input`. Accepts `retriever: VectorStoreRetriever`. |
| `services/chain/agent/agent_chain_service.py` | `AgentChainService` — owns LangGraph-based agent via `create_agent()`. Builds system prompt dynamically — injects project path when available. Runs agent with full message history. |
| `services/chain/request.py` | `ChainRequest` Pydantic model — `history: list[BaseMessage]`, `user_input: str`, `mode: str`, `retriever: VectorStoreRetriever | None`, `project_path: str | None`. |
| `services/chain/response.py` | `ChainResponse` Pydantic model — `answer: str | None`, `error: str | None`. Methods: `has_answer()`, `has_error()`. |

---

## File Responsibilities — Services — Tools

| File | Contains |
|---|---|
| `services/tools/run_code/executor.py` | `CodeExecutor` — runs Python code via `subprocess`. Returns stdout or stderr. Timeout after 10 seconds. |
| `services/tools/run_code/tool.py` | `run_code` LangChain tool — executes Python code and returns output or error. |
| `services/tools/read_file/tool.py` | `read_file` LangChain tool — reads file contents at a given path. Returns error string if not found. |
| `services/tools/write_file/tool.py` | `write_file` LangChain tool — writes content to a file. Creates parent directories if needed. |
| `services/tools/list_directory/tool.py` | `list_directory` LangChain tool — recursively lists all files and subdirectories at a given path. Labels each entry as `[file]` or `[dir]`. |

---

## File Responsibilities — Services — Document Extractors

| File | Contains |
|---|---|
| `services/document_extractors/text/plain/controller.py` | `PlainTextExtractorController` — owns `allowed_extensions` passed at construction. Calls `PlainTextExtractorService.extract()`. Returns `PlainTextExtractorResponse`. |
| `services/document_extractors/text/plain/service.py` | `PlainTextExtractorService` — scans directory recursively. Loads matching files via `TextLoader`. Returns list of `Document`. |
| `services/document_extractors/text/plain/request.py` | `PlainTextExtractorRequest` Pydantic model — `directory_path: str`. |
| `services/document_extractors/text/plain/response.py` | `PlainTextExtractorResponse` Pydantic model — `documents: list[Document]`, `error: str | None`. Methods: `has_documents()`, `has_error()`. |

---

## File Responsibilities — Services — Chunking

| File | Contains |
|---|---|
| `services/chunking/code/controller.py` | `CodeChunkingController` — owns `chunk_size` and `chunk_overlap` passed at construction. Calls `CodeChunkingService.chunk()`. Returns `CodeChunkingResponse`. |
| `services/chunking/code/service.py` | `CodeChunkingService` — splits documents using `RecursiveCharacterTextSplitter.from_language(language="python")`. Returns list of `Document` chunks. |
| `services/chunking/code/request.py` | `CodeChunkingRequest` Pydantic model — `documents: list[Document]`. |
| `services/chunking/code/response.py` | `CodeChunkingResponse` Pydantic model — `chunks: list[Document]`, `error: str | None`. Methods: `has_chunks()`, `has_error()`. |

---

## File Responsibilities — Services — Embedding Generators

| File | Contains |
|---|---|
| `services/embedding_generators/openai/controller.py` | `OpenAIEmbeddingController` — calls `OpenAIEmbeddingService.embed()`. Returns `OpenAIEmbeddingResponse`. |
| `services/embedding_generators/openai/service.py` | `OpenAIEmbeddingService` — owns `OpenAIEmbeddings` instance. Exposes `embed()` and `get_embeddings_model()`. |
| `services/embedding_generators/openai/request.py` | `OpenAIEmbeddingRequest` Pydantic model — `chunks: list[Document]`. |
| `services/embedding_generators/openai/response.py` | `OpenAIEmbeddingResponse` Pydantic model — `embeddings: list[list[float]]`, `error: str | None`. Methods: `has_embeddings()`, `has_error()`. |

---

## File Responsibilities — Services — Vector Stores

| File | Contains |
|---|---|
| `services/vector_stores/faiss/controller.py` | `FAISSVectorStoreController` — calls `FAISSVectorStoreService.build_retriever()`. Returns `FAISSVectorStoreResponse`. |
| `services/vector_stores/faiss/service.py` | `FAISSVectorStoreService` — owns `OpenAIEmbeddings` instance. Builds FAISS vector store from chunks. Returns `VectorStoreRetriever`. |
| `services/vector_stores/faiss/request.py` | `FAISSVectorStoreRequest` Pydantic model — `chunks: list[Document]`. |
| `services/vector_stores/faiss/response.py` | `FAISSVectorStoreResponse` Pydantic model — `retriever: VectorStoreRetriever | None`, `error: str | None`. Methods: `has_retriever()`, `has_error()`. |

---

## File Responsibilities — Services — Wiring

| File | Contains |
|---|---|
| `services/service_composer.py` | `ServiceComposer` — reads `ConfigBundle`. Instantiates shared `ChatOpenAI` LLM. Instantiates all chain services, tools, and infrastructure controllers. Passes config primitives down — no config object passed beyond this point. Returns `ServiceBundle`. |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds `chain_controller`, `extractor_controller`, `chunking_controller`, `embedding_controller`, `vector_store_controller`, `tools`. |

---

## File Responsibilities — Configuration

| File | Contains |
|---|---|
| `conf/settings/app_config.py` | `AppConfig` — Pydantic BaseSettings from `.env.app`. Fields: `app_name: str`, `system_prompt: str`. |
| `conf/settings/openai_config.py` | `OpenAIConfig` — Pydantic BaseSettings from `.env.openai`. Fields: `openai_api_key: str`, `openai_model: str`, `temperature: float`, `max_tokens: int`. |
| `conf/settings/retriever_config.py` | `RetrieverConfig` — Pydantic BaseSettings from `.env.retriever`. Fields: `chunk_size: int`, `chunk_overlap: int`, `allowed_extensions: list[str]`, `embedding_model: str`. |
| `conf/settings/config_bundle.py` | `ConfigBundle` dataclass — holds `app: AppConfig`, `openai: OpenAIConfig`, `retriever: RetrieverConfig`. Exposes `load_config()` factory function. |
| `conf/env/.env.app` | `APP_NAME`, `SYSTEM_PROMPT` |
| `conf/env/.env.openai` | `OPENAI_API_KEY`, `OPENAI_MODEL`, `TEMPERATURE`, `MAX_TOKENS` |
| `conf/env/.env.openai.example` | Safe-to-commit template. API key value is empty. |
| `conf/env/.env.retriever` | `CHUNK_SIZE`, `CHUNK_OVERLAP`, `ALLOWED_EXTENSIONS`, `EMBEDDING_MODEL` |
| `conf/env/.env.retriever.example` | Safe-to-commit template. |

---

## Key LangChain Concepts Introduced at Level 1

| Concept | Where It Lives | What You Learn |
|---|---|---|
| `ChatOpenAI` | `plain_chain_service.py` | How LangChain wraps the OpenAI API |
| `ChatPromptTemplate` | `plain_chain_service.py` | How to define system + human message templates |
| `MessagesPlaceholder` | `plain_chain_service.py` | How to inject chat history into the prompt |
| LCEL `|` operator | `plain_chain_service.py` | How to chain prompt → llm → parser |
| `StrOutputParser` | `plain_chain_service.py` | How to extract plain text from LLM response |
| `HumanMessage` / `AIMessage` | `history_transformer.py` | How LangChain represents conversation history |

---

## Key LangChain Concepts Introduced at Level 2

| Concept | Where It Lives | What You Learn |
|---|---|---|
| `TextLoader` | `document_extractors/text/plain/service.py` | How LangChain loads text files as Documents |
| `RecursiveCharacterTextSplitter` | `chunking/code/service.py` | How code is split into chunks for retrieval |
| `OpenAIEmbeddings` | `embedding_generators/openai/service.py` | How text is converted to vectors |
| `FAISS.from_documents()` | `vector_stores/faiss/service.py` | How a vector store is built from chunks |
| `VectorStoreRetriever` | `vector_stores/faiss/service.py` | How semantic search is exposed as a retriever |
| LCEL retrieval chain | `retrieval_chain_service.py` | How retriever context is injected into the prompt |

---

## Key LangChain Concepts Introduced at Level 3

| Concept | Where It Lives | What You Learn |
|---|---|---|
| `@tool` decorator | `services/tools/*/tool.py` | How to define LangChain-compatible tools from Python functions |
| `create_agent()` | `agent_chain_service.py` | How LangGraph-based agents are created and invoked |
| Tool routing | `chain_controller.py` | How the agent decides which tool to call |
| Agent system prompt injection | `agent_chain_service.py` | How to inject dynamic context (project path) into agent behavior |
| `CodeExecutor` via subprocess | `run_code/executor.py` | How to safely execute code and capture output |

---

## Models Convention

> Use **Pydantic** only at service boundaries (data crossing in/out of a service layer).
> Use **dataclass** for all internal app models (`AppState`, `ChatMessage`).