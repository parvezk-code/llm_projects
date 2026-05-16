# services/graph/nodes/report_node.py

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from services.graph.state import GraphState


def make_report_node(llm: ChatOpenAI):

    def report_node(state: GraphState) -> dict:
        existing_report = state.get("report", "")

        if existing_report:
            message = AIMessage(content=existing_report)
            return {
                "messages": [message],
                "report": existing_report,
            }

        understanding = state.get("understanding", "")
        test_code = state.get("test_code", "")
        test_results = state.get("test_results", "")
        plan = state.get("plan", [])

        sections = []

        if understanding:
            sections.append(f"Code understanding:\n{understanding}")
        if test_code:
            sections.append(f"Generated tests:\n{test_code}")
        if test_results:
            sections.append(f"Test results:\n{test_results}")

        if not sections:
            report = "No information available to generate a report."
            message = AIMessage(content=report)
            return {"messages": [message], "report": report}

        prompt = (
            "You are a senior Python developer.\n"
            "Based on the following information write a concise report.\n"
            "Only include sections relevant to what was actually done.\n\n"
            + "\n\n".join(sections)
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        report = response.content

        message = AIMessage(content=report)
        return {
            "messages": [message],
            "report": report,
        }

    return report_node