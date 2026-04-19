import time
import webbrowser

import streamlit as st

from state.session_state import SessionState
from ui.page import PageUI
from ui.sidebar import SidebarUI
from ui.pdf_panel import PDFPanelUI
from ui.chat_panel import ChatPanelUI
from services.auth_service import AuthService
from services.pdf_service import PDFService
from services.llm_service import LLMService
from utils.file_utils import compute_hash

_LOGIN_TIMEOUT_SECONDS = 180


class AppController:
    """
    Orchestrates the full Streamlit render cycle.
    Reads from SessionState, delegates rendering to UI classes,
    and delegates business logic to service classes.
    """

    def __init__(
        self,
        state: SessionState,
        page_ui: PageUI,
        sidebar_ui: SidebarUI,
        pdf_ui: PDFPanelUI,
        chat_ui: ChatPanelUI,
        auth_svc: AuthService,
        pdf_svc: PDFService,
        llm_svc: LLMService,
    ) -> None:
        self._state = state
        self._page_ui = page_ui
        self._sidebar_ui = sidebar_ui
        self._pdf_ui = pdf_ui
        self._chat_ui = chat_ui
        self._auth_svc = auth_svc
        self._pdf_svc = pdf_svc
        self._llm_svc = llm_svc

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        self._page_ui.configure_page()
        self._page_ui.render_title()
        default_auth_mode = (
            "ChatGPT" if self._auth_svc.load_stored_auth() else "API key"
        )
        self._state.init(
            default_auth_mode=default_auth_mode,
            default_oauth_model=self._auth_svc.default_model,
        )
        self._poll_login()
        self._handle_sidebar()
        self._handle_pdf_upload()
        self._handle_chat()

    # ------------------------------------------------------------------
    # OAuth polling
    # ------------------------------------------------------------------

    def _poll_login(self) -> None:
        handle = self._state.get_login_handle()
        if handle is None:
            return

        try:
            stored = self._auth_svc.poll_login(handle)
        except RuntimeError as e:
            self._state.set_login_handle(None)
            self._state.set_login_started_at(None)
            st.error(f"Sign-in failed: {e}")
            return

        if stored is not None:
            self._state.set_login_handle(None)
            self._state.set_login_started_at(None)
            st.success("Signed in with ChatGPT.")
            st.rerun()
            return

        started = self._state.get_login_started_at() or time.time()
        if time.time() - started > _LOGIN_TIMEOUT_SECONDS:
            self._auth_svc.cancel_login(handle)
            self._state.set_login_handle(None)
            self._state.set_login_started_at(None)
            st.error("Sign-in timed out. Try again.")
            return

        time.sleep(1.0)
        st.rerun()

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------

    def _handle_sidebar(self) -> None:
        stored_auth = self._auth_svc.load_stored_auth()
        event = self._sidebar_ui.render(
            stored_auth=stored_auth,
            current_mode=self._state.get_auth_mode(),
            current_model=self._state.get_oauth_model(),
            login_pending=self._state.get_login_handle() is not None,
            oauth_models=self._auth_svc.oauth_models,
        )

        # Persist widget selections back to state
        self._state.set_auth_mode(event.mode)
        if event.model:
            self._state.set_oauth_model(event.model)

        # React to button clicks
        if event.sign_in_clicked:
            self._start_login()

        if event.cancel_login_clicked:
            handle = self._state.get_login_handle()
            if handle:
                self._auth_svc.cancel_login(handle)
            self._state.set_login_handle(None)
            self._state.set_login_started_at(None)
            st.rerun()

        if event.sign_out_clicked:
            self._auth_svc.logout()
            st.rerun()

        if event.clear_conversation_clicked:
            self._state.clear_history()
            st.rerun()

        if event.remove_pdf_clicked:
            self._state.clear_doc()
            self._state.clear_history()
            st.rerun()

    def _start_login(self) -> None:
        try:
            handle = self._auth_svc.start_login()
        except OSError as e:
            st.error(
                f"Could not start local callback server on port "
                f"{self._auth_svc.redirect_port}: {e}"
            )
            return
        self._state.set_login_handle(handle)
        self._state.set_login_started_at(time.time())
        webbrowser.open(handle.authorize_url)
        st.rerun()

    # ------------------------------------------------------------------
    # PDF upload
    # ------------------------------------------------------------------

    def _handle_pdf_upload(self) -> None:
        pdf_bytes = self._pdf_ui.render_uploader(self._state.get_uploader_key())

        if pdf_bytes is None:
            return

        incoming_hash = compute_hash(pdf_bytes)

        # Skip re-extraction if the same file is still uploaded
        if self._state.get_doc_hash() == incoming_hash:
            doc = self._state.get_doc()
        else:
            with st.spinner("Extracting text..."):
                try:
                    doc = self._pdf_svc.extract(pdf_bytes)
                except RuntimeError as e:
                    self._pdf_ui.render_extraction_error(str(e))
                    return

            self._state.set_doc(doc, incoming_hash)
            self._state.clear_history()

        # Render metadata for the loaded doc
        self._pdf_ui.render_metadata(
            page_count=doc.page_count,
            used_ocr=doc.used_ocr,
            char_count=len(doc.text),
        )
        if self._llm_svc.check_truncation(doc.text):
            self._pdf_ui.render_truncation_warning()

    # ------------------------------------------------------------------
    # Chat
    # ------------------------------------------------------------------

    def _handle_chat(self) -> None:
        doc = self._state.get_doc()
        self._chat_ui.render_history(self._state.get_history())
        prompt = self._chat_ui.render_chat_input(doc_ready=doc is not None)

        if not prompt:
            return

        if doc is None:
            self._chat_ui.render_no_pdf_warning()
            return

        # Snapshot history before appending the new user message
        prior_history = list(self._state.get_history())
        self._state.append_message("user", prompt)
        self._chat_ui.render_user_message(prompt)

        with self._chat_ui.thinking_spinner():
            try:
                reply = self._llm_svc.chat(
                    history=prior_history,
                    pdf_text=doc.text,
                    prompt=prompt,
                    auth_mode=self._state.get_auth_mode(),
                    oauth_model=self._resolve_oauth_model(),
                )
            except RuntimeError as e:
                reply = f"**Error:** {e}"
            except Exception as e:
                reply = f"**Error calling OpenAI:** {e}"

        self._chat_ui.render_assistant_reply(reply)
        self._state.append_message("assistant", reply)

    def _resolve_oauth_model(self) -> str | None:
        if self._state.get_auth_mode() != "ChatGPT":
            return None
        if self._auth_svc.load_stored_auth() is None:
            return None
        return self._state.get_oauth_model() or self._auth_svc.default_model
