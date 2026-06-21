# desktop/actions/chat/send_message_action.py

from core.models.chat_message import ChatMessage
from core.models.pdf_document import PDFDocument

from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle


class SendMessageAction:
    """
    Workflow: send the user's question to the LLM with the loaded PDF as
    context, and record the exchange.

    Steps: read the document and history from state, assemble the provider
    message list (system prompt + history + new question), call the chat
    gateway, then commit BOTH turns to state only after a successful reply
    (so a failed call leaves state unchanged). Returns the user and assistant
    messages for the Event Handler to render.

    The ChatMessage -> dict conversion lives here, in the Action.
    """

    def __init__(self, state_controller: StateController, gateways: GatewayBundle):
        self._state = state_controller
        self._gateways = gateways

    def execute(self, user_text: str) -> tuple[ChatMessage, ChatMessage]:
        self._state.set_processing(True)
        try:
            document = self._state.get_document()
            history = self._state.get_chat_messages()
            user_message = ChatMessage.user(user_text)

            messages = self._build_messages(document, history, user_message)
            reply_text = self._gateways.chat.get_reply(messages)   # gateway -> Core
            assistant_message = ChatMessage.assistant(reply_text)

            # commit both turns only after a successful reply (atomic)
            self._state.add_chat_message(user_message)
            self._state.add_chat_message(assistant_message)

            return user_message, assistant_message
        finally:
            self._state.set_processing(False)

    # --- Message assembly (one task each) ---

    def _build_messages(
        self,
        document: PDFDocument | None,
        history: list[ChatMessage],
        user_message: ChatMessage,
    ) -> list[dict]:
        messages = [{"role": "system", "content": self._build_system_prompt(document)}]
        for message in history:
            messages.append({"role": message.role, "content": message.content})
        messages.append({"role": user_message.role, "content": user_message.content})
        return messages

    def _build_system_prompt(self, document: PDFDocument | None) -> str:
        if document is None:
            return "You are a helpful assistant."
        return (
            "You are a helpful assistant. Answer the user's questions using the "
            "following document as context.\n\n"
            f"Document: {document.filename}\n\n"
            f"{document.text}"
        )

# desktop/actions/chat/send_message_action.py