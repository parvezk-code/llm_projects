# services/graph/nodes/generate_tests_node.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from services.graph.state import GraphState


def make_generate_tests_node(llm: ChatOpenAI):

    def generate_tests_node(state: GraphState) -> dict:
        understanding = state["understanding"]
        file_contents = state["file_contents"]

        files_text = "\n\n".join(
            f"### {filename}\n```python\n{content}\n```"
            for filename, content in file_contents.items()
        )

        prompt = (
            "You are a senior Python developer writing pytest tests.\n"
            "Based on the following code and understanding, write comprehensive pytest tests.\n"
            "Rules:\n"
            "- Use pytest only\n"
            "- Cover happy path and edge cases\n"
            "- Each test function must start with test_\n"
            "- Return only valid Python code, no markdown, no explanation\n\n"
            f"Understanding:\n{understanding}\n\n"
            f"Code:\n{files_text}"
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        test_code = response.content.strip()

        if test_code.startswith("```"):
            lines = test_code.split("\n")
            test_code = "\n".join(lines[1:-1])

        message = AIMessage(content=f"Tests generated:\n```python\n{test_code}\n```")
        return {
            "messages": [message],
            "test_code": test_code,
        }

    return generate_tests_node