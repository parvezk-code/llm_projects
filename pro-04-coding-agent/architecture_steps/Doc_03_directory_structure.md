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
├── application/
│   ├── __init__.py
│   ├── application_bundle
│   ├── clear_chat_command
│   ├── load_project_command
│   └── send_message_command
│
├── utils/     --->  worker.py
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
    │   └── worker.py
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
│   ├── chain_service.py
│   ├── request.py
│   └── response.py
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
| `app/main_controller.py` | Slim orchestrator. Builds UI via `UIComposer`, services via `ServiceComposer`. Owns `AppState` and `StateController`. Instantiates all event handlers. Wires signals to handler methods via `_bind_signals()` using `bind_*` methods on controllers. |
| `app/event_handlers/chat/send_message_handler.py` | Handles a single chat turn. Reads user input via `UIBundle`. Reads history via `StateController`. Calls `history_transformer` to convert history. Builds `ChainRequest`. Starts `Worker` (QThread). On result: saves messages via `StateController`, appends bubbles to chat area, re-enables input. On error: shows status bar, rolls back user message. Owns `_retriever` — set externally via `set_retriever()` when RAG mode is active. |
| `app/event_handlers/chat/clear_chat_handler.py` | Clears history, error, and project path via `StateController`. Empties chat area. Hides status bar. Resets toolbar project label. |
| `app/event_handlers/project/load_project_handler.py` | Handles project folder selection. Disables UI. Starts `Worker` with `_build_retriever()` method. On result: checks `response.has_error()` — on success sets project path in state, sets retriever on `SendMessageHandler`, updates toolbar project label, re-enables UI — on error shows status bar error message, re-enables UI. |
| `app/event_handlers/business_logic/worker.py` | Generic `Worker(QThread)` — accepts any callable `method` and `on_result` callback. Calls `method()` in background thread. Emits `result_ready` signal with full response object. Handler is responsible for checking `response.has_error()`. |

---

## File Responsibilities — App State

| File | Contains |
|---|---|
| `app/state/models/chat_message.py` | `ChatMessage` dataclass — `role: str` and `content: str`. Internal model. Not Pydantic. |
| `app/state/app_state.py` | `AppState` dataclass — `messages: list[ChatMessage]`, `error: str | None`, `project_path: str | None`. |
| `app/state/state_controller.py` | `StateController` — owns all reads and writes to `AppState`. Exposes `add_message()`, `get_messages()`, `pop_last_message()`, `clear_history()`, `has_messages()`, `set_error()`, `clear_error()`, `get_error()`, `set_project_path()`, `get_project_path()`, `has_project()`, `clear_project()`. |

---

## File Responsibilities — Event Handler Transformers

| File | Contains |
|---|---|
| `app/event_handlers/transformers/chain/history_transformer.py` | `convert_history(messages: list[ChatMessage]) → list[BaseMessage]`. Pure function. Converts internal `ChatMessage` dataclasses to LangChain `HumanMessage` / `AIMessage` types. Called by `SendMessageHandler` before building `ChainRequest`. |

---

## File Responsibilities — UI Layer

| File | Contains |
|---|---|
| `ui/ui_composer.py` | `UIComposer` — builds all components and controllers. Assembles main window layout. Returns `UIBundle`. |
| `ui/ui_bundle.py` | `UIBundle` frozen dataclass — holds refs to `ToolbarController`, `FolderPickerController`, `ChatAreaController`, `InputBarController`, `StatusBarController`. |
| `ui/toolbar/toolbar_component.py` | Toolbar UI — Clear button, Load Project button, project label. Emits `clear_clicked` and `load_project_clicked` signals. Exposes accessors: `set_project_name()`, `clear_project_name()`, `set_enabled()`, `set_clear_enabled()`. |
| `ui/toolbar/toolbar_controller.py` | Manages `ToolbarComponent`. Exposes `bind_clear_clicked()`, `bind_load_project_clicked()`. Operation methods: `set_enabled()`, `set_clear_enabled()`, `set_project_name()`, `clear_project_label()`. |
| `ui/toolbar/widgets/clear_button_widget.py` | Clear chat QPushButton widget. |
| `ui/toolbar/widgets/load_project_button_widget.py` | Load Project QPushButton widget. |
| `ui/toolbar/widgets/project_label_widget.py` | QLabel showing loaded project folder name. Exposes `set_project_name()` and `clear_project_name()`. |
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
| `services/chain/chain_controller.py` | `ChainController` — receives `ChainRequest`. Calls `ChainService.run()`. Returns `ChainResponse`. |
| `services/chain/chain_service.py` | `ChainService` — owns plain LCEL chain and retrieval LCEL chain. Plain chain: `prompt | llm | output_parser`. Retrieval chain: `input_map | prompt | llm | output_parser` using `lambda` extractors for `context`, `history`, `input`. Accepts `retriever: VectorStoreRetriever | None`. System prompt owned internally. |
| `services/chain/request.py` | `ChainRequest` Pydantic model — `history: list[BaseMessage]`, `user_input: str`, `retriever: VectorStoreRetriever | None`. |
| `services/chain/response.py` | `ChainResponse` Pydantic model — `answer: str | None`, `error: str | None`. Methods: `has_answer()`, `has_error()`. |

---

## File Responsibilities — Services — Retriever

| File | Contains |
|---|---|
| `services/retriever/pipeline/controller.py` | `RetrieverPipelineController` — receives `RetrieverPipelineRequest`. Calls `RetrieverPipelineService.build()`. Returns `RetrieverPipelineResponse`. |
| `services/retriever/pipeline/service.py` | `RetrieverPipelineService` — orchestrates 3 stages in sequence: extract → chunk → vector store. Raises `RuntimeError` on stage failure. Returns `VectorStoreRetriever`. |
| `services/retriever/pipeline/request.py` | `RetrieverPipelineRequest` Pydantic model — `project_path: str`. |
| `services/retriever/pipeline/response.py` | `RetrieverPipelineResponse` Pydantic model — `retriever: VectorStoreRetriever | None`, `error: str | None`. Methods: `has_retriever()`, `has_error()`. |

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
| `services/service_composer.py` | `ServiceComposer` — reads `ConfigBundle`. Instantiates all services and controllers. Passes config primitives down — no config object passed beyond this point. Returns `ServiceBundle`. |
| `services/service_bundle.py` | `ServiceBundle` frozen dataclass — holds `chain_controller`, `retriever_controller`, `extractor_controller`, `chunking_controller`, `embedding_controller`, `vector_store_controller`. |

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
| `ChatOpenAI` | `chain_service.py` | How LangChain wraps the OpenAI API |
| `ChatPromptTemplate` | `chain_service.py` | How to define system + human message templates |
| `MessagesPlaceholder` | `chain_service.py` | How to inject chat history into the prompt |
| LCEL `|` operator | `chain_service.py` | How to chain prompt → llm → parser |
| `StrOutputParser` | `chain_service.py` | How to extract plain text from LLM response |
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
| LCEL retrieval chain | `chain_service.py` | How retriever context is injected into the prompt |


---

## Models Convention

> Use **Pydantic** only at service boundaries (data crossing in/out of a service layer).
> Use **dataclass** for all internal app models (`AppState`, `ChatMessage`).