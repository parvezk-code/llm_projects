# tools/get_working_directory/controller.py

from pathlib import Path

from tools.get_working_directory.settings import working_directory_settings
from tools.get_working_directory.response import (
    GetWorkingDirectoryResponse,
    GetWorkingDirectorySuccessResponse,
    GetWorkingDirectoryErrorResponse,
)


class GetWorkingDirectoryController:

    def execute(self) -> GetWorkingDirectoryResponse:
        try:
            path = Path(working_directory_settings.WORKING_DIRECTORY).expanduser().resolve()

            if not path.exists():
                return GetWorkingDirectoryErrorResponse(
                    error_type="DirectoryNotFound",
                    error_message=f"Working directory does not exist: {path}",
                )

            if not path.is_dir():
                return GetWorkingDirectoryErrorResponse(
                    error_type="NotADirectory",
                    error_message=f"Path is not a directory: {path}",
                )

            return GetWorkingDirectorySuccessResponse(
                directory_path=str(path),
            )

        except Exception as error:
            return GetWorkingDirectoryErrorResponse(
                error_type="UnexpectedError",
                error_message=str(error),
            )