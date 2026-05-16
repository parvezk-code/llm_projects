# services/graph/nodes/understand_node.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from services.graph.state import GraphState


def make_understand_node(llm: ChatOpenAI):

    def understand_node(state: GraphState) -> dict:
        file_contents = state["file_contents"]

        files_text = "\n\n".join(
            f"### {filename}\n```python\n{content}\n```"
            for filename, content in file_contents.items()
        )

        prompt = (
            "You are a senior Python developer.\n"
            "Analyse the following Python files and provide a concise summary of:\n"
            "1. What each file does\n"
            "2. Key functions and classes\n"
            "3. How the files relate to each other\n\n"
            f"{files_text}"
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        understanding = response.content

        message = AIMessage(content=f"Understanding complete:\n{understanding}")
        return {
            "messages": [message],
            "understanding": understanding,
        }

    return understand_node