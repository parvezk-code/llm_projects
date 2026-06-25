# desktop_local/main.py

import sys
from PyQt6.QtWidgets import QApplication

from utils.logger import configure_logging
from conf.settings.config_bundle import load_config

from core.services.chat.plain_chat_service import PlainChatService
from core.services.chat.retrieval_chat_service import RetrievalChatService
from core.services.chat.agent_chat_service import AgentChatService
from core.services.extraction.document_extractor_service import DocumentExtractorService
from core.services.chunking.code_chunker_service import CodeChunkerService
from core.services.embedding.openai_embedding_service import OpenAIEmbeddingService
from core.services.vector_store.faiss_vector_store_service import FaissVectorStoreService

from core.services.tools.list_directory_tool import list_directory
from core.services.tools.read_file_tool import read_file
from core.services.tools.write_file_tool import write_file
from core.services.tools.run_tests_tool import run_tests
from core.services.tools.run_code_tool import run_code

from desktop.gateways.chat_gateway import ChatGateway
from desktop.gateways.index_gateway import IndexGateway
from desktop.gateways.agent_gateway import AgentGateway
from desktop.gateways.gateway_bundle import GatewayBundle
from desktop.main_controller import MainController


AGENT_SYSTEM_PROMPT = (
    "You are an expert Python coding agent. You can explore the user's project, "
    "read and write files, run code, and run tests using the available tools. "
    "Use the tools to complete the user's request, then summarise what you did."
)


def build_local_gateways(config) -> GatewayBundle:
    """LOCAL mode: build Gateways that wrap Core services directly."""
    # --- chat services ---
    plain_chat_service = PlainChatService(
        api_key=config.openai.api_key,
        model=config.openai.model,
        temperature=config.openai.llm_temperature,
        max_tokens=config.openai.llm_max_tokens,
    )
    retrieval_chat_service = RetrievalChatService(
        api_key=config.openai.api_key,
        model=config.openai.model,
        temperature=config.openai.llm_temperature,
        max_tokens=config.openai.llm_max_tokens,
    )

    # --- RAG pipeline services ---
    extractor = DocumentExtractorService(
        extensions=tuple(config.retriever.allowed_extensions),
    )
    chunker = CodeChunkerService(
        chunk_size=config.retriever.chunk_size,
        overlap=config.retriever.chunk_overlap,
    )
    embedding_service = OpenAIEmbeddingService(
        api_key=config.openai.api_key,
        model=config.retriever.embedding_model,
    )
    vector_store = FaissVectorStoreService(embedding_service)

    # --- agent service (tools + tool-using agent) ---
    tools = [list_directory, read_file, write_file, run_tests, run_code]
    agent_chat_service = AgentChatService(
        api_key=config.openai.api_key,
        model=config.openai.model,
        temperature=config.openai.llm_temperature,
        max_tokens=config.openai.llm_max_tokens,
        system_prompt=AGENT_SYSTEM_PROMPT,
        tools=tools,
    )

    # --- gateways ---
    chat_gateway = ChatGateway(plain_chat_service, retrieval_chat_service)
    index_gateway = IndexGateway(extractor, chunker, vector_store)
    agent_gateway = AgentGateway(agent_chat_service)

    return GatewayBundle(chat=chat_gateway, index=index_gateway, agent=agent_gateway)


def main() -> None:
    configure_logging()

    app = QApplication(sys.argv)

    try:
        config = load_config()
    except Exception as error:
        print(
            f"Configuration error: {error}\n\n"
            "Set your OpenAI key in conf/env/.env.local:\n"
            "  api_key=sk-...\n"
            "You can copy conf/env/.env.openAI.example as a starting point.",
            file=sys.stderr,
        )
        sys.exit(1)

    app.setApplicationName(config.app.app_name)

    gateways = build_local_gateways(config)     # LOCAL mode decided here only
    controller = MainController(gateways)
    controller.start()                          # builds UI, wires events, applies theme, shows window

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# desktop_local/main.py