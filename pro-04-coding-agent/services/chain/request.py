# services/chain/request.py

from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class ChainRequest(BaseModel):
    """
    Input to ChainController.
    Pydantic because it crosses the service boundary.

    system_prompt : the agent's persona and instructions
    history       : full conversation so far as LangChain BaseMessage list.
                    Conversion from internal ChatMessage types happens in the
                    transformer layer before this request is built.
    user_input    : the new message from the user
    """
    system_prompt: str
    history: list[BaseMessage]
    user_input: str
    model_config = {"arbitrary_types_allowed": True}