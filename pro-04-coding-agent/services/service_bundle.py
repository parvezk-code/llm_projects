from dataclasses import dataclass
from services.chain.chain_controller import ChainController


@dataclass(frozen=True)
class ServiceBundle:
    """
    Frozen dataclass holding all service-layer controllers.
    Passed from ServiceComposer → MainController → event handlers.

    At Level 1: only ChainController.
    At Level 2: will add RetrieverController.
    At Level 3: will add ToolExecutorController.
    """
    chain_controller: ChainController
