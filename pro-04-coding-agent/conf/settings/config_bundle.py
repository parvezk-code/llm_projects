from dataclasses import dataclass
from conf.settings.app_config import AppConfig
from conf.settings.openai_config import OpenAIConfig


@dataclass
class ConfigBundle:
    app: AppConfig
    openai: OpenAIConfig


def load_config() -> ConfigBundle:
    """Instantiate and return all config objects. Called once in main.py."""
    return ConfigBundle(
        app=AppConfig(),
        openai=OpenAIConfig(),
    )
