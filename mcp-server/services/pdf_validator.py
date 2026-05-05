# services/pdf_validator.py

from pathlib import Path
from conf.settings import settings


class PDFValidator:

    def validate(self, pdf_path: str) -> str | None:
        path = Path(pdf_path).expanduser().resolve()

        if not path.exists():
            return f"PDF file does not exist: {path}"

        if not path.is_file():
            return f"Path is not a file: {path}"

        if path.suffix.lower() not in settings.ALLOWED_EXTENSIONS:
            return f"File is not an allowed type: {path.suffix}"

        if path.stat().st_size == 0:
            return f"File is empty: {path}"

        if path.stat().st_size > settings.max_file_size_bytes:
            return f"File exceeds maximum size of {settings.MAX_FILE_SIZE_MB}MB: {path}"

        return None