# conf/settings/mcp.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPConfig(BaseSettings):
    mcp_server_url: str = "http://localhost:8000/mcp"

    model_config = SettingsConfigDict(
        env_file=(
            "conf/env/.env.mcp",
            "conf/env/.env.local",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )