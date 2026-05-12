import logging
from conf.settings.config_bundle import ConfigBundle
from services.chain.chain_controller import ChainController
from services.service_bundle import ServiceBundle

logger = logging.getLogger(__name__)


class ServiceComposer:
    """
    Instantiates all service-layer controllers and wires them together.
    Returns a ServiceBundle.

    ChainController now owns ChainService instantiation internally,
    so ServiceComposer only needs to pass OpenAIConfig to ChainController.
    """

    @staticmethod
    def compose( config: ConfigBundle ) -> ServiceBundle:
        logger.debug( "ServiceComposer: building services" )

        # Controller reads config and wires ChainService internally
        chain_controller = ChainController( config.openai )

        logger.debug( "ServiceComposer: done" )
        return ServiceBundle( chain_controller=chain_controller )