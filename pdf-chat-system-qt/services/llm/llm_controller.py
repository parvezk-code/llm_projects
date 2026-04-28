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
            # Convert history to raw dicts for LLMService
            history_dicts = [
                {"role": msg.role, "content": msg.content}
                for msg in transaction.history
            ]

            raw_response = self._service.call(
                pdf_text=transaction.pdf_text,
                history=history_dicts,
                user_message=transaction.user_message.content
            )

            transaction.response = ChatMessage(
                role="assistant",
                content=raw_response
            )

            return transaction

        except Exception as e:
            raise LLMCallError(
                f"Could not reach OpenAI API. Check your connection."
            ) from e