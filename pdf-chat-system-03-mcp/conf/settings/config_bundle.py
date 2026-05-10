# conf/settings/config_bundle.py

from conf.settings.appConfig import AppConfig
from conf.settings.openAI import OpenAIConfig
from conf.settings.mcp import MCPConfig


class AppSettings:
    """Aggregates all application settings."""

    def __init__(self):
        self.appConfig = AppConfig()
        self.llm = OpenAIConfig()
        self.mcpConfig = MCPConfig()
