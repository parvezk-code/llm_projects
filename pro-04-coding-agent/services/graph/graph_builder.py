# services/graph/graph_builder.py

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from services.graph.state import GraphState
from services.graph.nodes.plan_node import make_plan_node
from services.graph.nodes.read_node import read_node
from services.graph.nodes.understand_node import make_understand_node
from services.graph.nodes.generate_tests_node import make_generate_tests_node
from services.graph.nodes.save_tests_node import save_tests_node
from services.graph.nodes.run_tests_node import run_tests_node
from services.graph.nodes.report_node import make_report_node


def _route_after_plan(state: GraphState) -> str:
    plan = state.get("plan", [])
    if "read" in plan:
        return "read"
    if "run_tests" in plan:
        return "run_tests"
    return "report"


def _route_after_read(state: GraphState) -> str:
    plan = state.get("plan", [])
    if "understand" in plan:
        return "understand"
    return "report"


def _route_after_understand(state: GraphState) -> str:
    plan = state.get("plan", [])
    if "generate_tests" in plan:
        return "generate_tests"
    return "report"


def _route_after_generate_tests(state: GraphState) -> str:
    plan = state.get("plan", [])
    if "save_tests" in plan:
        return "save_tests"
    return "report"


def _route_after_save_tests(state: GraphState) -> str:
    plan = state.get("plan", [])
    if "run_tests" in plan:
        return "run_tests"
    return "report"


def _route_after_run_tests(state: GraphState) -> str:
    return "report"


class GraphBuilder:

    def __init__(self, llm: ChatOpenAI) -> None:
        self._llm = llm

    def build(self):
        builder = StateGraph(GraphState)

        builder.add_node("plan", make_plan_node(self._llm))
        builder.add_node("read", read_node)
        builder.add_node("understand", make_understand_node(self._llm))
        builder.add_node("generate_tests", make_generate_tests_node(self._llm))
        builder.add_node("save_tests", save_tests_node)
        builder.add_node("run_tests", run_tests_node)
        builder.add_node("report", make_report_node(self._llm))

        builder.set_entry_point("plan")

        builder.add_conditional_edges("plan", _route_after_plan, {
            "read": "read",
            "run_tests": "run_tests",
            "report": "report",
        })
        builder.add_conditional_edges("read", _route_after_read, {
            "understand": "understand",
            "report": "report",
        })
        builder.add_conditional_edges("understand", _route_after_understand, {
            "generate_tests": "generate_tests",
            "report": "report",
        })
        builder.add_conditional_edges("generate_tests", _route_after_generate_tests, {
            "save_tests": "save_tests",
            "report": "report",
        })
        builder.add_conditional_edges("save_tests", _route_after_save_tests, {
            "run_tests": "run_tests",
            "report": "report",
        })
        builder.add_conditional_edges("run_tests", _route_after_run_tests, {
            "report": "report",
        })
        builder.add_edge("report", END)

        memory = MemorySaver()
        return builder.compile(checkpointer=memory)