# tools/list_pdfs_in_directory/directory_scanner.py

from pathlib import Path

from tools.list_pdfs_in_directory.settings import list_pdfs_settings


class DirectoryScanner:

    def scan(self, path: Path) -> list[str]:
        pdf_files = [
            str(file)
            for file in sorted(path.iterdir())
            if file.is_file() and file.suffix.lower() in list_pdfs_settings.ALLOWED_EXTENSIONS
        ]

        return pdf_files