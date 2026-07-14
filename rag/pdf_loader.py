from pathlib import Path

import fitz

from core.logger import app_logger


class PDFLoader:
    def load(self, file_path: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported"
            )

        app_logger.info(
            f"Loading PDF: {path.name}"
        )

        document = fitz.open(path)

        try:
            pages: list[str] = []

            for page in document:
                text = page.get_text("text").strip()

                if text:
                    pages.append(text)

            content = "\n\n".join(pages)

            app_logger.success(
                f"PDF loaded successfully: {path.name}"
            )

            return content

        finally:
            document.close()


pdf_loader = PDFLoader()