# services/chain/response.py

from pydantic import BaseModel


class ChainResponse(BaseModel):
    answer: str | None = None
    error: str | None = None

    def has_answer(self) -> bool:
        return self.answer is not None

    def has_error(self) -> bool:
        return self.error is not None