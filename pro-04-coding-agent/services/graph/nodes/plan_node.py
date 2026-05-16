# services/graph/nodes/plan_node.py

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from services.graph.state import GraphState


def make_plan_node(llm: ChatOpenAI):

    def plan_node(state: GraphState) -> dict:
        user_input = state["user_input"]
        project_path = state["project_path"]

        prompt = (
            "You are a coding assistant that analyses user instructions.\n"
            "Given a user instruction and a project path, decide:\n"
            "1. Which nodes to run from: read, understand, generate_tests, save_tests, run_tests, report\n"
            "2. Which specific files to target (empty list means all files)\n\n"
            "Rules:\n"
            "- If user asks to analyse or understand code: include read, understand, report\n"
            "- If user asks to generate tests: include read, understand, generate_tests, save_tests, report\n"
            "- If user asks to run tests: include run_tests, report\n"
            "- If user asks to generate AND run tests: include all nodes\n"
            "- If user input is unrelated to code analysis or testing: return only report with a message\n"
            "- Extract specific filenames mentioned by the user into target_files\n"
            "- If no specific file mentioned, return empty list for target_files\n\n"
            "Respond ONLY with a valid JSON object like this:\n"
            "{\n"
            '  "plan": ["read", "understand", "report"],\n'
            '  "target_files": ["utils.py"],\n'
            '  "off_topic_message": ""\n'
            "}\n"
            "off_topic_message is only filled when the input is unrelated to coding tasks.\n\n"
            f"User instruction: {user_input}\n"
            f"Project path: {project_path}"
        )

        response = llm.invoke([HumanMessage(content=prompt)])
        raw = response.content.strip()

        try:
            if raw.startswith("```"):
                lines = raw.split("\n")
                raw = "\n".join(lines[1:-1])
            parsed = json.loads(raw)
            plan = parsed.get("plan", ["report"])
            target_files = parsed.get("target_files", [])
            off_topic_message = parsed.get("off_topic_message", "")
        except Exception:
            plan = ["report"]
            target_files = []
            off_topic_message = "I could not understand your instruction. Please try again."

        if off_topic_message:
            plan = ["report"]

        message = AIMessage(content=f"Plan: {plan} | Target files: {target_files}")
        return {
            "messages": [message],
            "plan": plan,
            "target_files": target_files,
            "report": off_topic_message,
        }

    return plan_node