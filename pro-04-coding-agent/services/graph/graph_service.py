# services/graph/graph_service.py

from langchain_openai import ChatOpenAI
from services.graph.graph_builder import GraphBuilder


class GraphService:

    def __init__(self, llm: ChatOpenAI) -> None:
        self._graph = GraphBuilder(llm).build()

    def run(self, project_path: str, user_input: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "messages": [],
            "user_input": user_input,
            "project_path": project_path,
            "plan": [],
            "target_files": [],
            "file_contents": {},
            "understanding": "",
            "test_code": "",
            "test_file_path": "",
            "test_results": "",
            "report": "",
        }

        result = self._graph.invoke(initial_state, config=config)
        return result["report"]