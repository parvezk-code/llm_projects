# services/service_composer.py

from services.document_extractors.pdf.pymupdf.controller import PyMuPDFController
from services.document_extractors.pdf.pymupdf.service import PyMuPDFService

from services.llm.llm_service import LLMService
from services.llm.llm_controller import LLMController
from services.llm.utils.openai_formatter import OpenAIFormatter

from services.mcp.clients.client_sync import SyncConnection
from services.mcp.executor.controller import MCPToolController

from services.service_bundle import ServiceBundle
from conf.settings.config_bundle import AppSettings


class ServiceComposer:

    def build(self) -> ServiceBundle:

        # --- Load settings ---
        settings = AppSettings()

        # --- Build PDF extractor ---
        pdf_service    = PyMuPDFService()
        pdf_controller = PyMuPDFController(pdf_service)

        # --- Build MCP client, service, registry and controller ---
        mcp_client     = SyncConnection(settings.mcpConfig.mcp_server_url)
        mcp_controller = MCPToolController(mcp_client)

        # --- Build LLM service and controller ---
        available_tools = OpenAIFormatter().format_tool_definitions(mcp_controller.get_tools_list())
        llm_service    = LLMService(
            api_key     = settings.llm.api_key,
            model       = settings.llm.model,
            temperature = settings.llm.llm_temperature,
            max_tokens  = settings.llm.llm_max_tokens,
        )
        llm_controller = LLMController(llm_service, available_tools)

        # --- Return frozen bundle ---
        return ServiceBundle(
            pdf = pdf_controller,
            llm = llm_controller,
            mcp = mcp_controller
        )