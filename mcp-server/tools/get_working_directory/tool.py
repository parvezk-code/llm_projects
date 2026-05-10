# tools/get_working_directory/tool.py

from tools.get_working_directory.controller import GetWorkingDirectoryController
from tools.get_working_directory.response import GetWorkingDirectoryResponse


controller = GetWorkingDirectoryController()


def get_working_directory() -> GetWorkingDirectoryResponse:
    """Returns the working directory path where PDF files are present."""

    return controller.execute()
