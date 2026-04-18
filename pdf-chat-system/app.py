import hashlib
import time
import webbrowser

import streamlit as st

import auth
from llm_client import chat, fit_pdf_to_context
from pdf_extractor import ExtractedDoc, extract


st.set_page_config(page_title="PDF Chat", page_icon="📄")
st.title("Chat with a PDF")


def _file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _init_state() -> None:
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("uploader_key", 0)
    st.session_state.setdefault("auth_mode", "ChatGPT" if auth.load_auth() else "API key")
    st.session_state.setdefault("oauth_model", auth.DEFAULT_OAUTH_MODEL)
    st.session_state.setdefault("login_handle", None)
    st.session_state.setdefault("login_started_at", None)


def _reset_pdf() -> None:
    for k in ("doc", "doc_hash", "history"):
        st.session_state.pop(k, None)
    st.session_state["uploader_key"] += 1


def _poll_login() -> None:
    handle: auth.LoginHandle | None = st.session_state.get("login_handle")
    if handle is None:
        return
    try:
        stored = handle.poll()
    except RuntimeError as e:
        st.session_state["login_handle"] = None
        st.session_state["login_started_at"] = None
        st.error(f"Sign-in failed: {e}")
        return

    if stored is not None:
        st.session_state["login_handle"] = None
        st.session_state["login_started_at"] = None
        st.success("Signed in with ChatGPT.")
        st.rerun()
        return

    started = st.session_state.get("login_started_at") or time.time()
    if time.time() - started > 180:
        handle.cancel()
        st.session_state["login_handle"] = None
        st.session_state["login_started_at"] = None
        st.error("Sign-in timed out. Try again.")
        return

    time.sleep(1.0)
    st.rerun()


def _auth_panel() -> None:
    st.header("Auth")
    stored = auth.load_auth()

    mode = st.radio(
        "Mode",
        options=["ChatGPT", "API key"],
        key="auth_mode",
        horizontal=True,
    )

    if mode == "ChatGPT":
        if stored is None:
            if st.session_state.get("login_handle") is not None:
                st.info("Complete sign-in in your browser. Waiting for callback…")
                if st.button("Cancel sign-in"):
                    st.session_state["login_handle"].cancel()
                    st.session_state["login_handle"] = None
                    st.session_state["login_started_at"] = None
                    st.rerun()
            else:
                if st.button("Sign in with ChatGPT"):
                    try:
                        handle = auth.start_login()
                    except OSError as e:
                        st.error(
                            f"Could not start local callback server on port {auth.OAUTH_REDIRECT_PORT}: {e}"
                        )
                        return
                    st.session_state["login_handle"] = handle
                    st.session_state["login_started_at"] = time.time()
                    webbrowser.open(handle.authorize_url)
                    st.rerun()
        else:
            label = stored.email or stored.account_id or "ChatGPT account"
            st.caption(f"Signed in as **{label}**")
            st.selectbox(
                "Model",
                options=list(auth.OAUTH_MODELS),
                key="oauth_model",
                help="All Codex-addressable models. Not every slug is active on every plan; if one 400s, try another.",
            )
            if st.button("Sign out"):
                auth.logout()
                st.rerun()
    else:
        if stored is not None:
            st.caption("ChatGPT tokens are still stored. They will be ignored while API key mode is active.")
        st.caption("Using `OPENAI_API_KEY` and `OPENAI_MODEL` from `.env`.")


def _sidebar() -> None:
    with st.sidebar:
        _auth_panel()
        st.divider()
        st.header("Session")
        if st.button("Clear conversation"):
            st.session_state["history"] = []
            st.rerun()
        if st.button("Remove PDF"):
            _reset_pdf()
            st.rerun()


def _render_pdf_panel() -> ExtractedDoc | None:
    uploaded = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        key=f"uploader_{st.session_state['uploader_key']}",
    )
    if uploaded is None:
        return None

    data = uploaded.getvalue()
    h = _file_hash(data)
    if st.session_state.get("doc_hash") != h:
        with st.spinner("Extracting text..."):
            try:
                doc = extract(data)
            except RuntimeError as e:
                st.error(str(e))
                return None
        st.session_state["doc"] = doc
        st.session_state["doc_hash"] = h
        st.session_state["history"] = []

    doc: ExtractedDoc = st.session_state["doc"]
    method = "OCR" if doc.used_ocr else "PyPDF"
    st.caption(
        f"{doc.page_count} pages · extracted via {method} · {len(doc.text):,} chars"
    )

    _, truncated = fit_pdf_to_context(doc.text)
    if truncated:
        st.warning(
            "PDF exceeds the context budget; later pages were truncated. "
            "v1 has no retrieval — consider a smaller PDF."
        )
    return doc


def _resolve_oauth_model() -> str | None:
    if st.session_state.get("auth_mode") != "ChatGPT":
        return None
    if auth.load_auth() is None:
        return None
    return st.session_state.get("oauth_model") or auth.DEFAULT_OAUTH_MODEL


def main() -> None:
    _init_state()
    _sidebar()
    _poll_login()
    doc = _render_pdf_panel()

    for msg in st.session_state["history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    placeholder = "Ask a question about the PDF" if doc else "Upload a PDF to start"
    prompt = st.chat_input(placeholder)
    if not prompt:
        return
    if doc is None:
        st.warning("Upload a PDF first.")
        return

    prior_history = list(st.session_state["history"])
    st.session_state["history"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply = chat(prior_history, doc.text, prompt, oauth_model=_resolve_oauth_model())
            except RuntimeError as e:
                reply = f"**Error:** {e}"
            except Exception as e:
                reply = f"**Error calling OpenAI:** {e}"
        st.markdown(reply)

    st.session_state["history"].append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
