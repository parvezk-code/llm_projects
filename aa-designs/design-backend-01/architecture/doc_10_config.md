
```
  conf/                      
    ├── settings/
    │   ├── __init__.py
    │   ├── app_config.py
    │   ├── openai_config.py
    │   └── config_bundle.py
    └── env/
        ├── .env.app
        ├── .env.openai
        └── .env.openai.example

```

# Rules

- Bundle consistency. config_bundle.py aggregating the settings
- Use pydantic for config classes. It raises a clear error at startup if it's missing