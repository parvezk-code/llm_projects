# services/document_extractors/text/plain/response.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class PlainTextResponse:
    full_text: Optional[str] = None
    error: Optional[str] = None

    def has_error(self) -> bool:
        return self.error is not None

    def has_content(self) -> bool:
        return self.full_text is not None and len(self.full_text.strip()) > 0
