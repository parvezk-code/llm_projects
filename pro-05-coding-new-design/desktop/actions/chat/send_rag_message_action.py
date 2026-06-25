# desktop/actions/chat/send_rag_message_action.py

import logging
from core.models.chat_message import ChatMessage, Role
from core.models.chunk import Chunk
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class SendRagMessageAction:
    """
    Workflow: RAG chat — retrieve relevant chunks, then generate with context.
    Single-purpose: assumes an index exists (the handler guards the no-index case).

    1. Set is_processing (reset in finally).
    2. Read the stored ProjectIndex from state.
    3. Retrieve top chunks via the index gateway.
    4. Shape the context block (chunks -> text) and the provider message list HERE
       (transport shaping is the Action's job, not the gateway's or service's).
    5. Call chat gateway (RAG path).
    6. Commit both messages atomically only on success.
    7. Return (user_message, assistant_message).
    """

    SYSTEM_PROMPT = (
        "You are an expert Python coding assistant answering questions about the "
        "user's loaded project. Use the provided context from the project to ground "
        "your answer. If the context is insufficient, say so plainly."
    )

    def __init__(self, state: StateController, gateways: GatewayBundle) -> None:
        self._state = state
        self._gateways = gateways

    def execute(self, user_text: str) -> tuple[ChatMessage, ChatMessage]:
        self._state.set_processing(True)
        try:
            index = self._state.get_project_index()
            history = self._state.get_chat_messages()

            logger.debug("SendRagMessageAction: input=%r", user_text)
            chunks = self._gateways.index.retrieve(user_text, index)
            logger.debug("SendRagMessageAction: retrieved %d chunks", len(chunks))

            context_block = self._build_context(chunks)
            messages = self._build_messages(history, user_text, context_block)

            reply_text = self._gateways.chat.get_rag_reply(messages)
            logger.debug("SendRagMessageAction: reply length=%d", len(reply_text))

            user_msg = ChatMessage.user(user_text)
            assistant_msg = ChatMessage.assistant(reply_text)

            self._state.add_chat_message(user_msg)
            self._state.add_chat_message(assistant_msg)

            return user_msg, assistant_msg

        except Exception:
            logger.exception("SendRagMessageAction: failed — state unchanged")
            raise
        finally:
            self._state.set_processing(False)

    def _build_context(self, chunks: list[Chunk]) -> str:
        if not chunks:
            return "(no relevant context found)"
        blocks = []
        for i, chunk in enumerate(chunks, start=1):
            blocks.append(f"[{i}] {chunk.source_path}\n{chunk.content}")
        return "\n\n".join(blocks)

    def _build_messages(
        self,
        history: list[ChatMessage],
        user_text: str,
        context_block: str,
    ) -> list[dict]:
        system_content = f"{self.SYSTEM_PROMPT}\n\nProject context:\n{context_block}"
        messages = [{"role": "system", "content": system_content}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": Role.USER, "content": user_text})
        return messages

# desktop/actions/chat/send_rag_message_action.py