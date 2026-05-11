# services/document_extractors/text/plain/service.py


class PlainTextService:

    def extract_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
