from pydantic import BaseModel


class ChainResponse(BaseModel):
    """
    Output from ChainController.
    Pydantic because it crosses the service boundary.

    answer : the assistant's reply text (None if error occurred)
    error  : error message string (None if successful)
    """
    answer: str | None = None
    error: str | None = None

    def has_answer(self) -> bool:
        return self.answer is not None

    def has_error(self) -> bool:
        return self.error is not None
