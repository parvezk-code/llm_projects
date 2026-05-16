# services/graph/response.py

from pydantic import BaseModel


class GraphResponse(BaseModel):
    report: str | None = None
    error: str | None = None

    def has_report(self) -> bool:
        return self.report is not None

    def has_error(self) -> bool:
        return self.error is not None