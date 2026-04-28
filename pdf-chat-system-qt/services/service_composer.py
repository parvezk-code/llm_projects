# services/service_composer.py

from services.pdf.pdf_service import PDFService
from services.pdf.pdf_controller import PDFController
from services.llm.llm_service import LLMService
from services.llm.llm_controller import LLMController
from services.service_bundle import ServiceBundle
from config.settings import Settings


class ServiceComposer:

    def build(self) -> ServiceBundle:

        # --- Load settings ---
        settings = Settings()

        # --- Build PDF service and controller ---
        pdf_service    = PDFService()
        pdf_controller = PDFController(pdf_service)

        # --- Build LLM service and controller ---
        llm_service    = LLMService(api_key=settings.openai_api_key, model=settings.openai_model)
        llm_controller = LLMController(llm_service)

        # --- Return frozen bundle ---
        return ServiceBundle(
            pdf=pdf_controller,
            llm=llm_controller
        )