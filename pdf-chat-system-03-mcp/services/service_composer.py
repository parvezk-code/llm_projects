# services/service_composer.py

from services.pdf.pdf_service import PDFService
from services.pdf.pdf_controller import PDFController
from services.llm.llm_service import LLMService
from services.llm.llm_controller import LLMController
from services.service_bundle import ServiceBundle
from conf.settings.config_bundle import AppSettings
from services.mcp.clients.client_sync import SyncConnection
from services.mcp.controller import MCPToolController
from services.llm.utils.openai_formatter import OpenAIFormatter

class ServiceComposer:

    def build(self) -> ServiceBundle:

        # --- Load settings ---
        settings = AppSettings()

        # --- Build PDF service and controller ---
        pdf_service    = PDFService()
        pdf_controller = PDFController(pdf_service)

        # --- Build MCP Client service and controller ---
        mcp_client     = SyncConnection(settings.mcpConfig.mcp_server_url)
        mcp_controller = MCPToolController(mcp_client)
        available_tools= OpenAIFormatter().format_tool_definitions(mcp_controller.get_tools_list())
        
        # --- Build LLM service and controller ---
        llm_service    = LLMService(
            api_key     = settings.llm.api_key,
            model       = settings.llm.model,
            temperature = settings.llm.llm_temperature,
            max_tokens  = settings.llm.llm_max_tokens,
        )
        llm_controller = LLMController(llm_service, available_tools)

        # --- Return frozen bundle ---
        return ServiceBundle(
            pdf=pdf_controller,
            llm=llm_controller,
            mcp=mcp_controller
        )