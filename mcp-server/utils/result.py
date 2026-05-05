# utils/result.py

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Result:
    success: bool
    value: Any = field(default=None)
    error_type: str | None = field(default=None)
    error_message: str | None = field(default=None)

    @staticmethod
    def ok(value: Any = None) -> "Result":
        return Result(success=True, value=value)

    @staticmethod
    def fail(error_type: str, error_message: str) -> "Result":
        return Result(
            success=False,
            error_type=error_type,
            error_message=error_message,
        )