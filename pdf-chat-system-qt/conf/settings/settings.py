from conf.settings.appConfig import AppConfig
from conf.settings.openAI import OpenAIConfig


class AppSettings:
    """Aggregates all application settings."""

    def __init__(self):
        self.llm = OpenAIConfig()
        self.appConfig = AppConfig()
