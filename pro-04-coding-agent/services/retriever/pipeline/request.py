# services/retriever/pipeline/request.py

from pydantic import BaseModel


class RetrieverPipelineRequest(BaseModel):
    project_path: str