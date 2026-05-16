# services/graph/state.py

from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class GraphState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_input: str
    project_path: str
    plan: list[str]
    target_files: list[str]
    file_contents: dict[str, str]
    understanding: str
    test_code: str
    test_file_path: str
    test_results: str
    report: str