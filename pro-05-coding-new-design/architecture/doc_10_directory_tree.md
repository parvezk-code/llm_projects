# Directory Tree — Reference

The project layout, as a top-level tree plus one detailed tree per top-level
directory. Reflects the build through Level 3 (Tools & Agents). `__init__.py` and
`__pycache__` are omitted for readability.

---

## Top-Level

```text
coding-agent/
├── conf/             # typed configuration + env files (launcher reads only)
├── core/             # business logic: domain models + services (provider specifics)
├── desktop/          # mode-agnostic runtime: state, gateways, actions, handlers, root
├── desktop_local/    # LOCAL launcher + entry point (builds gateways, decides mode)
├── ui/               # presentation: components, controllers, pages, composition, styles
├── utils/            # cross-cutting helpers (logging)
└── docs/             # design rule documents
```

Dependency direction (downward only):

```text
ui → desktop/event_handlers → desktop/actions → state_controller + gateways → core
conf → (launcher only)
```

---

## conf/

Typed settings consumed only by the launcher. Secrets in `.env.local` (gitignored);
non-secret defaults committed.

```text
conf/
├── settings/
│   ├── app_config.py         # AppConfig
│   ├── openai_config.py      # OpenAIConfig (api_key required, no default)
│   ├── retriever_config.py   # RetrieverConfig (chunking/embedding/retrieval)
│   └── config_bundle.py      # ConfigBundle (frozen) + load_config()
└── env/
    ├── .env.app              # non-secret app settings        (committed)
    ├── .env.openAI.example   # template documenting LLM keys  (committed)
    ├── .env.retriever        # non-secret RAG settings        (committed)
    └── .env.local            # secrets + overrides            (gitignored, user-made)
```

---

## core/

Business logic and domain data. Independent of all upper layers; runs unchanged in
local or remote mode. Owns all third-party library specifics.

```text
core/
├── models/                          # passive, frozen domain data
│   ├── chat_message.py              # ChatMessage (+ Role) + factory constructors
│   ├── document.py                  # Document (one extracted source file)
│   ├── chunk.py                     # Chunk (embeddable/retrievable unit)
│   └── project_index.py             # ProjectIndex (opaque FAISS handle wrapper)
└── services/                        # single-capability operations
    ├── chat/
    │   ├── plain_chat_service.py        # plain LLM generation
    │   ├── retrieval_chat_service.py    # RAG generation with context
    │   └── agent_chat_service.py        # tool-using agent (create_agent)
    ├── extraction/
    │   └── document_extractor_service.py  # walk folder → Documents
    ├── chunking/
    │   └── code_chunker_service.py        # Documents → Chunks (language-aware)
    ├── embedding/
    │   └── openai_embedding_service.py    # OpenAI embeddings wrapper
    ├── vector_store/
    │   └── faiss_vector_store_service.py  # build + search FAISS
    └── tools/                             # agent tools (module-level @tool fns)
        ├── list_directory_tool.py
        ├── read_file_tool.py
        ├── write_file_tool.py
        ├── run_tests_tool.py              # pytest subprocess (30s)
        ├── run_code_tool.py               # uses CodeExecutor
        └── code_executor.py               # CodeExecutor (subprocess, 10s)
```

---

## desktop/

Mode-agnostic application runtime. State, gateways, actions, event handlers, and the
composition root. Knows nothing about local-vs-remote mode.

```text
desktop/
├── state/
│   └── app_state.py                  # AppState — data only (messages, processing,
│                                     #   project_path, project_index)
├── state_controller/
│   └── state_controller.py           # single access point; event-shaped methods
├── gateways/                         # thin delegating boundaries to Core
│   ├── chat_gateway.py               # get_reply, get_rag_reply
│   ├── index_gateway.py              # build_index, retrieve
│   ├── agent_gateway.py              # get_agent_reply
│   └── gateway_bundle.py             # GatewayBundle (frozen) — built by launcher
├── actions/                          # one workflow per file, organised by topic
│   ├── chat/
│   │   ├── send_plain_message_action.py
│   │   ├── send_rag_message_action.py
│   │   ├── send_agent_message_action.py
│   │   └── clear_chat_action.py
│   └── project/
│       └── load_project_action.py
├── action_bundles/
│   └── action_bundle.py              # ActionBundle (frozen) — built by MainController
├── event_handlers/                   # one dir per emitting component, one file per event
│   ├── input_bar/
│   │   └── send_router_handler.py    # on_send router + on_send_<mode> methods
│   ├── toolbar/
│   │   ├── clear_chat_handler.py     # on_clear_clicked
│   │   └── load_project_handler.py   # on_load_project_clicked
│   ├── folder_picker/
│   │   └── folder_selected_handler.py # on_folder_selected
│   ├── status_bar/
│   │   └── dismiss_handler.py        # on_dismissed
│   └── utils/
│       └── worker.py                 # QThread wrapper (on_result / on_error)
└── main_controller.py                # composition root; start() startup sequence
```

---

## desktop_local/

The LOCAL launcher and entry point. The only place config is loaded and mode is
decided.

```text
desktop_local/
└── main.py    # load_config → build Core services → build_local_gateways
            #   → MainController(gateways).start() → Qt exec
```

A future `desktop_remote/main.py` would mirror this, building gateways that wrap an
API client instead of Core directly — the only difference between modes.

---

## ui/

Presentation. Dumb components, their controllers, pages, the composition root
(ScreenManager), styles, and the StyleManager. Mode-agnostic; identical across
launchers.

```text
ui/
├── chat_area/                        # display-only component (no signals)
│   ├── chat_area_component.py
│   └── widgets/
│       ├── message_bubble_widget.py
│       └── placeholder_widget.py
├── input_bar/
│   ├── input_bar_component.py        # emits send_triggered
│   └── widgets/
│       ├── text_input_widget.py
│       └── send_button_widget.py
├── toolbar/
│   ├── toolbar_component.py          # emits clear_clicked, load_project_clicked, mode_changed
│   └── widgets/
│       ├── clear_button_widget.py
│       ├── load_project_button_widget.py
│       ├── mode_combo_widget.py
│       └── project_label_widget.py
├── status_bar/
│   └── status_bar_component.py       # emits dismiss_clicked
├── folder_picker/
│   └── folder_picker_component.py    # emits folder_selected
├── controllers/                      # one controller per component
│   ├── chat_area_controller.py
│   ├── input_bar_controller.py
│   ├── toolbar_controller.py
│   ├── status_bar_controller.py
│   └── folder_picker_controller.py
├── pages/
│   └── chat_page.py                  # builds components + controllers + layout
├── styles/
│   └── ocean_blue.qss                # external QSS theme
├── screen_manager.py                 # UI composition root → returns UIBundle
├── main_window.py                    # QMainWindow shell (single central widget)
├── ui_bundle.py                      # UIBundle (frozen) — controllers only
└── style_manager.py                  # loads + applies a .qss theme
```

---

## utils/

Cross-cutting helpers with no layer ownership.

```text
utils/
└── logger.py    # configure_logging()
```

---

## docs/

Design rule documents (one per layer) plus the generic architecture set.

```text
docs/
├── action_rules.md
├── gateway_rules.md
├── core_rules.md
├── config_rules.md
├── main_controller_rules.md
├── event_handler_rules.md
├── state_and_controller_rules.md
├── ui_component_and_controller_rules.md
└── directory_tree.md                 # this file
```

# Directory Tree — Reference