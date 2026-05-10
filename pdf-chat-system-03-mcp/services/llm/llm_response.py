# services/llm/llm_response.py


class LLMResponse:

    def __init__(self):
        self.final_answer: str | None        = None
        self.tool_calls:   list[dict] | None = None
        self.error:        str | None        = None

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def add_answer(self, answer: str) -> None:
        """Store the final text answer from the LLM."""
        self.final_answer = answer

    def add_tool_calls(self, tool_calls: list[dict]) -> None:
        """Store the list of tool calls requested by the LLM."""
        self.tool_calls = tool_calls

    def add_error(self, error: str) -> None:
        """Store an error message; clears answer and tool_calls."""
        self.error        = error
        self.final_answer = None
        self.tool_calls   = None

    # ------------------------------------------------------------------ #
    #  Convenience checks                                                  #
    # ------------------------------------------------------------------ #

    def has_tool_calls(self) -> bool:
        return self.tool_calls is not None and len(self.tool_calls) > 0

    def has_answer(self) -> bool:
        return self.final_answer is not None

    def has_error(self) -> bool:
        return self.error is not None