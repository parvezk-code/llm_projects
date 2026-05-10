# tools/list_pdfs_in_directory/tool.py

from pydantic import ValidationError

from tools.list_pdfs_in_directory.request import ListPDFsRequest
from tools.list_pdfs_in_directory.response import (
    ListPDFsResponse,
    ListPDFsErrorResponse,
)
from tools.list_pdfs_in_directory.controller import ListPDFsController


controller = ListPDFsController()


def list_pdfs_in_directory(directory_path: str) -> ListPDFsResponse:
    """List all PDF files present in the given directory."""

    try:
        request = ListPDFsRequest(directory_path=directory_path)

    except ValidationError as error:
        return ListPDFsErrorResponse(
            error_type="ValidationError",
            error_message=str(error),
        )

    return controller.execute(request)
