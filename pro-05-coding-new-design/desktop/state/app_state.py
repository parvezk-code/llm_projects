# desktop/state/app_state.py

from dataclasses import dataclass, field
from core.models.chat_message import ChatMessage
from core.models.project_index import ProjectIndex


@dataclass
class AppState:
    """
    Holds all current application data.
    Plain fields only — no methods, no logic.

    Level 2: 'mode' is gone (mode lives in the toolbar widget, read on demand).
    project_path / project_index hold the loaded RAG project and its built index.
    """
    messages: list[ChatMessage] = field(default_factory=list)
    is_processing: bool = False
    project_path: str | None = None
    project_index: ProjectIndex | None = None

# desktop/state/app_state.py