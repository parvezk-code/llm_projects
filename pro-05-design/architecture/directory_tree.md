
```

root/
├── __init__.py
├── main.py
├── requirements.txt
│
├── app/                     # Application layer
│   ├── __init__.py
│   ├── application.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── chat_controller.py
│   │   ├── session_controller.py
│   │   └── settings_controller.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── agent_service.py
│   │   ├── memory_service.py
│   │   └── settings_service.py
│   │
│   └── state/
│       ├── __init__.py
│       ├── app_state.py
│       ├── chat_state.py
│       └── session_state.py
│
├── domain/                  # Pure business logic
│   ├── __init__.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── chat_agent.py
│   │   └── coding_agent.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── message.py
│   │   ├── conversation.py
│   │   └── settings.py
│   │
│   └── workflows/
│       ├── __init__.py
│       ├── chat_workflow.py
│       └── coding_workflow.py
│
├── infrastructure/          # External systems
│   ├── __init__.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   ├── ollama_client.py
│   │   └── anthropic_client.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── sqlite_repository.py
│   │   ├── file_repository.py
│   │   └── settings_repository.py
│   │
│   └── logging/
│       ├── __init__.py
│       └── logger.py
│
├── ui/
│   ├── __init__.py
│   │
│   ├── windows/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── settings_window.py
│   │
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── chat_panel.py
│   │   ├── message_list.py
│   │   ├── input_panel.py
│   │   └── sidebar.py
│   │
│   ├── dialogs/
│   │   ├── __init__.py
│   │   └── about_dialog.py
│   │
│   └── resources/
│       ├── icons/
│       └── images/
│
├── conf/
│   ├── app_config.json
│   ├── model_config.json
│   └── logging_config.json
│
├── styles/
│   ├── main.qss
│   ├── variables.qss
│   └── widgets/
│       ├── chat_panel.qss
│       ├── sidebar.qss
│       └── buttons.qss
│
├── data/
│   ├── chats/
│   ├── cache/
│   └── settings/
│
├── tests/
│   ├── test_chat_service.py
│   ├── test_agent_service.py
│   └── test_controllers.py
│
└── docs/
    ├── architecture.md
    └── api.md


```