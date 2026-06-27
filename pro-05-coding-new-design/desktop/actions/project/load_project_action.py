# desktop/actions/project/load_project_action.py

import logging
from core.models.project_index import ProjectIndex
from desktop.state_controller.state_controller import StateController
from desktop.gateways.gateway_bundle import GatewayBundle

logger = logging.getLogger(__name__)


class LoadProjectAction:
    """
    Workflow: load a project folder and build its RAG index.

    1. Set is_processing (reset in finally).
    2. Build the index via the index gateway (extraction → chunking → embedding → store).
    3. Commit project path + index to state atomically only on success.
    4. Clear the chat (fresh conversation for the new project).
    5. Return the ProjectIndex to the handler.
    """

    def __init__(self, state: StateController, gateways: GatewayBundle) -> None:
        self._state = state
        self._gateways = gateways

    def execute(self, project_path: str) -> ProjectIndex:
        self._state.set_processing(True)
        try:
            logger.debug("LoadProjectAction: building index for %r", project_path)
            index = self._gateways.index.build_index(project_path)
            logger.debug("LoadProjectAction: indexed %d chunks", index.chunk_count)

            # Commit only after a successful build
            self._state.reset_on_project_loaded(project_path, index)

            return index

        except Exception:
            logger.exception("LoadProjectAction: failed — state unchanged")
            raise
        finally:
            self._state.set_processing(False)

# desktop/actions/project/load_project_action.py