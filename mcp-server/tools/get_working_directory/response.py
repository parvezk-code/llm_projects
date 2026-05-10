# tools/get_working_directory/response.py

from typing import Literal
from pydantic import BaseModel


class GetWorkingDirectoryResponse(BaseModel):
    success: bool


class GetWorkingDirectorySuccessResponse(GetWorkingDirectoryResponse):
    success: Literal[True] = True
    directory_path: str


class GetWorkingDirectoryErrorResponse(GetWorkingDirectoryResponse):
    success: Literal[False] = False
    error_type: str
    error_message: str