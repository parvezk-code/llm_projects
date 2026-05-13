# services/chain/request.py

from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langchain_core.vectorstores import VectorStoreRetriever


class ChainRequest(BaseModel):
    history: list[BaseMessage]
    user_input: str
    retriever: VectorStoreRetriever | None = None

    model_config = {"arbitrary_types_allowed": True}