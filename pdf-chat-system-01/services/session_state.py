from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    # Only used by static analysers (mypy/pyright) — never imported at runtime.
    from services.auth import LoginHandle, StoredAuth
    from services.pdf_extractor import ExtractedDoc


class SessionState:
    """
    Single source of truth for all st.session_state reads and writes.
    No rendering, no business logic — pure state management.
    """

    # ------------------------------------------------------------------
    # Bootstrap
    # ------------------------------------------------------------------

    def init(self, default_auth_mode: str, default_oauth_model: str) -> None:
        """
        Initialise every key with a safe default (idempotent).
        Defaults are supplied by AppController so this class has no
        dependency on auth or pdf_extractor at runtime.
        """
        st.session_state.setdefault("history", [])
        st.session_state.setdefault("uploader_key", 0)
        st.session_state.setdefault("auth_mode", default_auth_mode)
        st.session_state.setdefault("oauth_model", default_oauth_model)
        st.session_state.setdefault("login_handle", None)
        st.session_state.setdefault("login_started_at", None)
        st.session_state.setdefault("doc", None)
        st.session_state.setdefault("doc_hash", None)

    # ------------------------------------------------------------------
    # PDF document
    # ------------------------------------------------------------------

    def get_doc(self) -> ExtractedDoc | None:
        return st.session_state.get("doc")

    def set_doc(self, doc: ExtractedDoc, doc_hash: str) -> None:
        st.session_state["doc"] = doc
        st.session_state["doc_hash"] = doc_hash

    def get_doc_hash(self) -> str | None:
        return st.session_state.get("doc_hash")

    def clear_doc(self) -> None:
        st.session_state["doc"] = None
        st.session_state["doc_hash"] = None
        self.increment_uploader_key()

    # ------------------------------------------------------------------
    # Chat history
    # ------------------------------------------------------------------

    def get_history(self) -> list[dict]:
        return st.session_state.get("history", [])

    def append_message(self, role: str, content: str) -> None:
        st.session_state["history"].append({"role": role, "content": content})

    def clear_history(self) -> None:
        st.session_state["history"] = []

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------

    def get_auth_mode(self) -> str:
        return st.session_state.get("auth_mode", "API key")

    def set_auth_mode(self, mode: str) -> None:
        st.session_state["auth_mode"] = mode

    def get_oauth_model(self) -> str:
        return st.session_state.get("oauth_model", "")

    def set_oauth_model(self, model: str) -> None:
        st.session_state["oauth_model"] = model

    def get_login_handle(self) -> LoginHandle | None:
        return st.session_state.get("login_handle")

    def set_login_handle(self, handle: LoginHandle | None) -> None:
        st.session_state["login_handle"] = handle

    def get_login_started_at(self) -> float | None:
        return st.session_state.get("login_started_at")

    def set_login_started_at(self, t: float | None) -> None:
        st.session_state["login_started_at"] = t

    # ------------------------------------------------------------------
    # File uploader key  (increment forces Streamlit to remount widget)
    # ------------------------------------------------------------------

    def get_uploader_key(self) -> int:
        return st.session_state.get("uploader_key", 0)

    def increment_uploader_key(self) -> None:
        st.session_state["uploader_key"] = self.get_uploader_key() + 1
