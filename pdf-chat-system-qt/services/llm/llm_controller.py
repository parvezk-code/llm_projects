# services/llm/llm_controller.py

from services.llm.llm_service import LLMService
from app.models.services.llm_transaction import LLMTransaction
from app.models.services.chat_message import ChatMessage


class LLMCallError(Exception):
    pass


class LLMController:

    def __init__(self, service: LLMService):
        self._service = service

    # --- Called by MainController ---

    def ask(self, transaction: LLMTransaction) -> LLMTransaction:
        try:
            messages = self._build_messages(transaction)
            raw_response = self._service.call(messages)
            transaction.response = ChatMessage(role="assistant", content=raw_response)
            return transaction

        except Exception as e:
            raise LLMCallError(
                "Could not reach OpenAI API. Check your connection."
            ) from e

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _build_messages(self, transaction: LLMTransaction) -> list[dict]:
        messages = [{"role": "system", "content": self._get_system_prompt(transaction.pdf_text)}]

        for msg in transaction.history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": transaction.user_message.content})

        return messages

    def _get_system_prompt(self, pdf_text: str) -> str:
        return (
            "You are a helpful assistant. "
            "Answer questions based on the following PDF document:\n\n"
            f"{pdf_text}"
        )
