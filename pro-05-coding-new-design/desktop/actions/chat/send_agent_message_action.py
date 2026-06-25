# desktop/actions/chat/send_agent_message_action.py

import logging
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from core.models.chat_message import ChatMessage, Role
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class SendAgentMessageAction:
    """
    Workflow: agent (tool-using) chat. Like RAG, this assumes a project is loaded
    (the handler guards the no-project case). The agent can list/read/write files,
    run code, and run tests within the loaded project.

    1. Set is_processing (reset in finally).
    2. Read history + project path from state.
    3. Shape history into LangChain messages HERE (transport shaping is the
       Action's job, not the gateway's or service's).
    4. Call the agent gateway (passes tools + project path through to Core).
    5. Commit both messages atomically only on success.
    6. Return (user_message, assistant_message).
    """

    def __init__(self, state: StateController, gateways: GatewayBundle) -> None:
        self._state = state
        self._gateways = gateways

    def execute(self, user_text: str) -> tuple[ChatMessage, ChatMessage]:
        self._state.set_processing(True)
        try:
            history = self._state.get_chat_messages()
            project_path = self._state.get_project_path()
            lc_history = self._to_langchain_messages(history)

            logger.debug("SendAgentMessageAction: input=%r", user_text)
            reply_text = self._gateways.agent.get_agent_reply(
                history=lc_history,
                user_input=user_text,
                project_path=project_path,
            )
            logger.debug("SendAgentMessageAction: reply length=%d", len(reply_text))

            user_msg = ChatMessage.user(user_text)
            assistant_msg = ChatMessage.assistant(reply_text)

            self._state.add_chat_message(user_msg)
            self._state.add_chat_message(assistant_msg)

            return user_msg, assistant_msg

        except Exception:
            logger.exception("SendAgentMessageAction: failed — state unchanged")
            raise
        finally:
            self._state.set_processing(False)

    def _to_langchain_messages(self, history: list[ChatMessage]) -> list[BaseMessage]:
        messages: list[BaseMessage] = []
        for msg in history:
            if msg.role == Role.USER:
                messages.append(HumanMessage(content=msg.content))
            elif msg.role == Role.ASSISTANT:
                messages.append(AIMessage(content=msg.content))
        return messages

# desktop/actions/chat/send_agent_message_action.py