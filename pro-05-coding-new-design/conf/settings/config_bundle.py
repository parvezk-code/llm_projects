# conf/settings/config_bundle.py

from dataclasses import dataclass
from conf.settings.app_config import AppConfig
from conf.settings.openai_config import OpenAIConfig


@dataclass(frozen=True)
class ConfigBundle:
    app: AppConfig
    openai: OpenAIConfig


def load_config() -> ConfigBundle:
    """
    Instantiates and validates all settings.
    Raises pydantic ValidationError if a required value (e.g. api_key) is missing.
    Called by the launcher only.
    """
    return ConfigBundle(
        app=AppConfig(),
        openai=OpenAIConfig(),
    )

# conf/settings/config_bundle.py