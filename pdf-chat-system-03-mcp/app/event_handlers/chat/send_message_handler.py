# app/event_handlers/chat/send_message_handler.py

import json
import logging

from app.models.services.llm_transaction.chat_message import ChatMessage
from app.models.state.app_state import AppState
from ui.ui_bundle import UIBundle
from services.service_bundle import ServiceBundle
from services.llm.llm_request import LLMRequest
from services.llm.llm_response import LLMResponse

log = logging.getLogger(__name__)

MAX_ROUNDS = 10

_SYSTEM_PROMPT_NO_PDF = (
    "You are a helpful assistant with access to a PDF document library. "
    "You have tools to: find the documents directory, list PDF files in it, "
    "and read the full text of any PDF. "
    "When the user asks about a document or its contents, use your tools "
    "to locate and read the relevant PDF before answering. "
    "Always answer from the actual document content."
)

_SYSTEM_PROMPT_WITH_PDF = (
    "You are a helpful assistant. "
    "The user has uploaded a PDF document. Its full text is provided below. "
    "Answer the user's question using this text as your primary source. "
    "You also have tools to find and read other PDFs from the document library "
    "if the uploaded PDF does not contain enough information to answer. "
    "\n\n"
    "=== UPLOADED PDF CONTENT ===\n"
    "{pdf_text}\n"
    "=== END OF UPLOADED PDF CONTENT ==="
)


def _build_system_prompt(pdf_text: str | None) -> str:
    if pdf_text:
        return _SYSTEM_PROMPT_WITH_PDF.format(pdf_text=pdf_text)
    return _SYSTEM_PROMPT_NO_PDF


class SendMessageHandler:

    def __init__(self, state: AppState, ui: UIBundle, svc: ServiceBundle):
        self._state = state
        self._ui    = ui
        self._svc   = svc

    # ------------------------------------------------------------------
    # Public
    # ------------------------------------------------------------------

    def on_send_clicked(self, text: str):
        pdf_text = self._state.pdf.full_text if self._state.pdf else None

        if pdf_text:
            log.info("PDF context available — injecting into system prompt")
        else:
            log.info("No PDF uploaded — LLM will use MCP tools")

        log.info("User question: %s", text)

        request = LLMRequest(
            system_prompt = _build_system_prompt(pdf_text),
            chat_history  = list(self._state.messages),
            user_question = text,
        )

        final_answer = self._run_agentic_loop(request)

        if final_answer is None:
            return

        user_msg      = ChatMessage(role="user",      content=text)
        assistant_msg = ChatMessage(role="assistant", content=final_answer)

        self._state.messages.append(user_msg)
        self._state.messages.append(assistant_msg)

        self._ui.chat_area.handleNewMessage(user_msg, assistant_msg)
        self._ui.toolbar.on_chat_updated()
        self._ui.input_bar.clear_input()

    # ------------------------------------------------------------------
    # Private — agentic loop
    # ------------------------------------------------------------------

    def _run_agentic_loop(self, request: LLMRequest) -> str | None:

        for round_number in range(1, MAX_ROUNDS + 1):
            log.debug("── Round %d: sending request to LLM", round_number)

            response: LLMResponse = self._svc.llm.ask_with_tools(request)

            if response.has_error():
                log.error("LLM error in round %d: %s", round_number, response.error)
                self._on_llm_failed(response.error)
                return None

            if response.has_answer():
                log.info(
                    "Round %d: final answer received — %.120s%s",
                    round_number,
                    response.final_answer,
                    "…" if len(response.final_answer) > 120 else "",
                )
                return response.final_answer

            if response.has_tool_calls():
                tool_names = [tc["function"]["name"] for tc in response.tool_calls]
                log.info("Round %d: LLM requested tools — %s", round_number, tool_names)
                self._execute_tool_round(request, response.tool_calls)
                continue

        log.error("Agentic loop exhausted after %d rounds with no final answer.", MAX_ROUNDS)
        self._on_llm_failed(
            f"No answer after {MAX_ROUNDS} rounds. The agent may be stuck in a tool loop."
        )
        return None

    def _execute_tool_round(self, request: LLMRequest, tool_calls: list[dict]) -> None:

        request.add_message({
            "role":       "assistant",
            "content":    None,
            "tool_calls": tool_calls,
        })

        for tool_call in tool_calls:
            tool_name    = tool_call["function"]["name"]
            arguments    = json.loads(tool_call["function"]["arguments"])
            tool_call_id = tool_call["id"]

            log.info("  Calling tool: %s  args: %s", tool_name, arguments)

            result = self._svc.mcp.call(tool_name, arguments)

            log.debug("  Tool result  [%s]: %s", tool_name, result)

            request.add_tool_result(tool_call_id, result)

    # ------------------------------------------------------------------
    # Private — error handling
    # ------------------------------------------------------------------

    def _on_llm_failed(self, message: str):
        self._state.error = message
        self._ui.status_bar.show_error(message)
        self._ui.toolbar.on_llm_call_failed()