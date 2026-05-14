# app/applications/send_message_command.py

from app.state.state_controller import StateController
from app.event_handlers.transformers.chain.history_transformer import convert_history
from services.chain.request import ChainRequest
from services.chain.response import ChainResponse
from services.service_bundle import ServiceBundle


class SendMessageCommand:

    def __init__(
        self,
        state: StateController,
        service: ServiceBundle,
    ) -> None:
        self._state = state
        self._service = service
        self._retriever = None

    def set_retriever(self, retriever: object) -> None:
        self._retriever = retriever

    def execute(self, user_input: str) -> ChainResponse:
        self._state.add_message(role="user", content=user_input)
        history = convert_history(self._state.get_messages()[:-1])
        request = ChainRequest(
            history=history,
            user_input=user_input,
            retriever=self._retriever if self._state.has_project() else None,
        )
        response = self._service.chain_controller.run(request)
        if response.has_error():
            self._state.pop_last_message()
        else:
            self._state.add_message(role="assistant", content=response.answer)
        return response