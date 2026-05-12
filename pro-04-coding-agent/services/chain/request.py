from pydantic import BaseModel
from app.models.services.llm_transaction.chat_message import ChatMessage


class ChainRequest(BaseModel):
    """
    Input to ChainController.
    Pydantic because it crosses the service boundary.

    system_prompt : the agent's persona and instructions
    history       : full conversation so far (ChatMessage list)
    user_input    : the new message from the user
    """
    system_prompt: str
    history: list[ChatMessage]
    user_input: str

    model_config = {"arbitrary_types_allowed": True}
