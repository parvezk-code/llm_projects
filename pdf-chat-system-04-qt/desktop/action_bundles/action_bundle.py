# desktop/action_bundles/action_bundle.py

from dataclasses import dataclass

from desktop.actions.chat.send_message_action import SendMessageAction
from desktop.actions.chat.clear_chat_action import ClearChatAction
from desktop.actions.document.upload_document_action import UploadDocumentAction


@dataclass(frozen=True)
class ActionBundle:
    """Single bundle of all application actions, handed to the Event Handlers."""

    send_message: SendMessageAction
    clear_chat: ClearChatAction
    upload_document: UploadDocumentAction

# desktop/action_bundles/action_bundle.py