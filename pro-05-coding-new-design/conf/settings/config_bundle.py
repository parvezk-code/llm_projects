# conf/settings/config_bundle.py

from dataclasses import dataclass
from conf.settings.app_config import AppConfig
from conf.settings.openai_config import OpenAIConfig


@dataclass
class ConfigBundle:
    app: AppConfig
    openai: OpenAIConfig


def load_config() -> ConfigBundle:
    return ConfigBundle(
        app=AppConfig(),
        openai=OpenAIConfig(),
    )