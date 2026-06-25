# conf/settings/config_bundle.py

from dataclasses import dataclass
from conf.settings.app_config import AppConfig
from conf.settings.openai_config import OpenAIConfig
from conf.settings.retriever_config import RetrieverConfig


@dataclass(frozen=True)
class ConfigBundle:
    app: AppConfig
    openai: OpenAIConfig
    retriever: RetrieverConfig


def load_config() -> ConfigBundle:
    """
    Instantiates and validates all settings.
    Raises pydantic ValidationError if a required value (e.g. api_key) is missing.
    Called by the launcher only.

    Level 2: adds RetrieverConfig.
    """
    return ConfigBundle(
        app=AppConfig(),
        openai=OpenAIConfig(),
        retriever=RetrieverConfig(),
    )

# conf/settings/config_bundle.py