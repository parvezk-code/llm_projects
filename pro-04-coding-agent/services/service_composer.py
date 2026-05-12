import logging
from conf.settings.config_bundle import ConfigBundle
from services.chain.chain_service import ChainService
from services.chain.chain_controller import ChainController
from services.service_bundle import ServiceBundle

logger = logging.getLogger(__name__)


class ServiceComposer:
    """
    Instantiates all service-layer objects and wires them together.
    Returns a ServiceBundle.

    Called once in main.py. Nothing else should instantiate services directly.
    """

    @staticmethod
    def compose(config: ConfigBundle) -> ServiceBundle:
        logger.debug("ServiceComposer: building services")

        chain_service = ChainService(config.openai)
        chain_controller = ChainController(chain_service)

        logger.debug("ServiceComposer: done")
        return ServiceBundle(chain_controller=chain_controller)
