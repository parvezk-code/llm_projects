# tools/list_pdfs_in_directory/controller.py

from pathlib import Path

from tools.list_pdfs_in_directory.request import ListPDFsRequest
from tools.list_pdfs_in_directory.response import (
    ListPDFsResponse,
    ListPDFsSuccessResponse,
    ListPDFsErrorResponse,
)
from tools.list_pdfs_in_directory.directory_scanner import DirectoryScanner


scanner = DirectoryScanner()


class ListPDFsController:

    def execute(self, request: ListPDFsRequest) -> ListPDFsResponse:
        try:
            path = Path(request.directory_path).expanduser().resolve()

            if not path.exists():
                return ListPDFsErrorResponse(
                    error_type="DirectoryNotFound",
                    error_message=f"Directory does not exist: {path}",
                )

            if not path.is_dir():
                return ListPDFsErrorResponse(
                    error_type="NotADirectory",
                    error_message=f"Path is not a directory: {path}",
                )

            pdf_files = scanner.scan(path)

            return ListPDFsSuccessResponse(
                directory_path=str(path),
                pdf_files=pdf_files,
                total_count=len(pdf_files),
            )

        except Exception as error:
            return ListPDFsErrorResponse(
                error_type="UnexpectedError",
                error_message=str(error),
            )
