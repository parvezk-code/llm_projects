import json
import os
import platform
import uuid

import httpx
from dotenv import load_dotenv
from openai import OpenAI

import auth

load_dotenv()


_SYSTEM_TEMPLATE = """You are an assistant that answers questions about the PDF provided below. Ground your answers in the PDF's content. If the answer isn't in the PDF, say so plainly rather than guessing.

<pdf>
{pdf_text}
</pdf>"""


_CHARS_PER_TOKEN = 4
_CONTEXT_TOKEN_BUDGET = 100_000


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file.")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    return OpenAI(api_key=api_key, base_url=base_url)


def _get_model() -> str:
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError(
            "OPENAI_MODEL is not set. Set it in .env "
            "(e.g. OPENAI_MODEL=gpt-4o-mini)."
        )
    return model


def fit_pdf_to_context(pdf_text: str) -> tuple[str, bool]:
    max_chars = _CONTEXT_TOKEN_BUDGET * _CHARS_PER_TOKEN
    if len(pdf_text) <= max_chars:
        return pdf_text, False
    return pdf_text[:max_chars], True


def chat(history: list[dict], pdf_text: str, user_msg: str, oauth_model: str | None = None) -> str:
    stored = auth.load_auth()
    if stored is not None:
        return _chat_via_oauth(stored, history, pdf_text, user_msg, oauth_model)
    return _chat_via_api_key(history, pdf_text, user_msg)


def _chat_via_api_key(history: list[dict], pdf_text: str, user_msg: str) -> str:
    client = _get_client()
    model = _get_model()

    trimmed, _ = fit_pdf_to_context(pdf_text)
    messages = [
        {"role": "system", "content": _SYSTEM_TEMPLATE.format(pdf_text=trimmed)},
        *history,
        {"role": "user", "content": user_msg},
    ]

    resp = client.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content or ""


def _to_responses_content(role: str, text: str) -> dict:
    content_type = "output_text" if role == "assistant" else "input_text"
    return {"role": role, "content": [{"type": content_type, "text": text}]}


def _chat_via_oauth(
    stored: auth.StoredAuth,
    history: list[dict],
    pdf_text: str,
    user_msg: str,
    oauth_model: str | None,
) -> str:
    stored = auth.refresh_if_needed(stored)
    model = oauth_model or auth.DEFAULT_OAUTH_MODEL

    trimmed, _ = fit_pdf_to_context(pdf_text)
    instructions = _SYSTEM_TEMPLATE.format(pdf_text=trimmed)

    input_items = []
    for msg in history:
        input_items.append(_to_responses_content(msg["role"], msg["content"]))
    input_items.append(_to_responses_content("user", user_msg))

    headers = {
        "Authorization": f"Bearer {stored.access_token}",
        "originator": auth.OAUTH_ORIGINATOR,
        "User-Agent": f"pdf-chat/0.1 ({platform.system().lower()})",
        "session_id": str(uuid.uuid4()),
        "Content-Type": "application/json",
    }
    if stored.account_id:
        headers["ChatGPT-Account-Id"] = stored.account_id

    body = {
        "model": model,
        "instructions": instructions,
        "input": input_items,
        "tools": [],
        "tool_choice": "auto",
        "parallel_tool_calls": True,
        "store": False,
        "stream": True,
        "include": [],
        "prompt_cache_key": str(uuid.uuid4()),
    }
    headers["Accept"] = "text/event-stream"

    chunks: list[str] = []
    with httpx.stream(
        "POST", auth.CODEX_API_ENDPOINT, headers=headers, json=body, timeout=120.0
    ) as resp:
        if resp.status_code >= 400:
            raise RuntimeError(f"Codex API error {resp.status_code}: {resp.read().decode('utf-8', 'replace')[:500]}")
        for line in resp.iter_lines():
            if not line or not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]" or not payload:
                continue
            try:
                event = json.loads(payload)
            except json.JSONDecodeError:
                continue
            etype = event.get("type", "")
            if etype == "response.output_text.delta":
                delta = event.get("delta")
                if isinstance(delta, str):
                    chunks.append(delta)
            elif etype == "response.completed" and not chunks:
                for item in event.get("response", {}).get("output", []) or []:
                    for c in item.get("content", []) or []:
                        if c.get("type") in ("output_text", "text"):
                            chunks.append(c.get("text", ""))

    return "".join(chunks)
