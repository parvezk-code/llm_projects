# conf/settings/config_bundle.py

from dataclasses import dataclass

from conf.settings.app_config import AppConfig
from conf.settings.openai_config import OpenAIConfig


@dataclass(frozen=True)
class ConfigBundle:
    """Aggregates all application settings into one object."""

    app: AppConfig
    openai: OpenAIConfig


def load_config() -> ConfigBundle:
    """Instantiate every settings group. Raises if required values are missing."""
    return ConfigBundle(
        app=AppConfig(),
        openai=OpenAIConfig(),
    )

# conf/settings/config_bundle.py