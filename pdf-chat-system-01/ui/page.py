import streamlit as st


class PageUI:
    """One-time page-level Streamlit configuration."""

    def configure_page(self) -> None:
        st.set_page_config(page_title="PDF Chat", page_icon="📄")

    def render_title(self) -> None:
        st.title("Chat with a PDF")
