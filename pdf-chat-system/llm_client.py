import os

from dotenv import load_dotenv
from openai import OpenAI

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


def chat(history: list[dict], pdf_text: str, user_msg: str) -> str:
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
