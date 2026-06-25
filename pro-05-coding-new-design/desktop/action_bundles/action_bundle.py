# desktop/action_bundles/action_bundle.py

from dataclasses import dataclass
from desktop.actions.chat.send_plain_message_action import SendPlainMessageAction
from desktop.actions.chat.send_rag_message_action import SendRagMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction
from desktop.actions.project.load_project_action import LoadProjectAction


@dataclass(frozen=True)
class ActionBundle:
    """
    Immutable bundle of all actions.
    Built by MainController; injected into Event Handlers.

    Level 2: send_message split into send_plain + send_rag; load_project added.
    """
    send_plain: SendPlainMessageAction
    send_rag: SendRagMessageAction
    clear_chat: ClearChatAction
    load_project: LoadProjectAction

# desktop/action_bundles/action_bundle.py