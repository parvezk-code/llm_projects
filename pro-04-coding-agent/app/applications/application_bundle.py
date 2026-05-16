# app/applications/application_bundle.py

from dataclasses import dataclass
from app.applications.send_message_command import SendMessageCommand
from app.applications.clear_chat_command import ClearChatCommand
from app.applications.load_project_command import LoadProjectCommand
from app.applications.run_graph_command import RunGraphCommand


@dataclass(frozen=True)
class ApplicationBundle:
    send_message: SendMessageCommand
    clear_chat: ClearChatCommand
    load_project: LoadProjectCommand
    run_graph: RunGraphCommand