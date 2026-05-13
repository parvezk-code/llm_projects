# core_services/document_extractors/text/plain/request.py

from pydantic import BaseModel


class PlainTextExtractorRequest(BaseModel):
    directory_path: str