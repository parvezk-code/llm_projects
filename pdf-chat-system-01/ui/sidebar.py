from dataclasses import dataclass

import streamlit as st


@dataclass
class SidebarEvent:
    """
    Raw values captured from every sidebar widget in a single render pass.
    The Controller reads these and decides what action to take.
    """
    # Auth panel
    mode: str = "API key"
    model: str = ""
    sign_in_clicked: bool = False
    sign_out_clicked: bool = False
    cancel_login_clicked: bool = False

    # Session panel
    clear_conversation_clicked: bool = False
    remove_pdf_clicked: bool = False


class SidebarUI:
    """
    Renders the entire sidebar and returns a SidebarEvent.
    Completely stateless — receives all values it needs as arguments.
    """

    def render(
        self,
        stored_auth,
        current_mode: str,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        event = SidebarEvent()

        with st.sidebar:
            event = self._render_auth_panel(
                event, stored_auth, current_mode, current_model, login_pending, oauth_models
            )
            st.divider()
            event = self._render_session_panel(event)

        return event

    # ------------------------------------------------------------------
    # Auth panel
    # ------------------------------------------------------------------

    def _render_auth_panel(
        self,
        event: SidebarEvent,
        stored_auth,
        current_mode: str,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        st.header("Auth")

        mode = st.radio(
            "Mode",
            options=["ChatGPT", "API key"],
            index=0 if current_mode == "ChatGPT" else 1,
            horizontal=True,
        )
        event.mode = mode

        if mode == "ChatGPT":
            event = self._render_chatgpt_auth(
                event, stored_auth, current_model, login_pending, oauth_models
            )
        else:
            self._render_api_key_auth(stored_auth)

        return event

    def _render_chatgpt_auth(
        self,
        event: SidebarEvent,
        stored_auth,
        current_model: str,
        login_pending: bool,
        oauth_models: list[str],
    ) -> SidebarEvent:
        if stored_auth is None:
            if login_pending:
                st.info("Complete sign-in in your browser. Waiting for callback…")
                event.cancel_login_clicked = st.button("Cancel sign-in")
            else:
                event.sign_in_clicked = st.button("Sign in with ChatGPT")
        else:
            label = stored_auth.email or stored_auth.account_id or "ChatGPT account"
            st.caption(f"Signed in as **{label}**")
            model = st.selectbox(
                "Model",
                options=oauth_models,
                index=oauth_models.index(current_model)
                if current_model in oauth_models
                else 0,
                help="All Codex-addressable models. Not every slug is active on every plan; if one 400s, try another.",
            )
            event.model = model
            event.sign_out_clicked = st.button("Sign out")

        return event

    @staticmethod
    def _render_api_key_auth(stored_auth) -> None:
        if stored_auth is not None:
            st.caption(
                "ChatGPT tokens are still stored. "
                "They will be ignored while API key mode is active."
            )
        st.caption("Using `OPENAI_API_KEY` and `OPENAI_MODEL` from `.env`.")

    # ------------------------------------------------------------------
    # Session panel
    # ------------------------------------------------------------------

    @staticmethod
    def _render_session_panel(event: SidebarEvent) -> SidebarEvent:
        st.header("Session")
        event.clear_conversation_clicked = st.button("Clear conversation")
        event.remove_pdf_clicked = st.button("Remove PDF")
        return event
