# desktop/action_bundles/action_bundle.py

from dataclasses import dataclass
from desktop.actions.chat.send_message_action import SendMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction


@dataclass(frozen=True)
class ActionBundle:
    """
    Immutable bundle of all actions.
    Built by MainController; injected into Event Handlers.
    """
    send_message: SendMessageAction
    clear_chat: ClearChatAction