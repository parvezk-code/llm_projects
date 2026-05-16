# services/graph/request.py

from pydantic import BaseModel


class GraphRequest(BaseModel):
    project_path: str
    user_input: str
    thread_id: str = "default"