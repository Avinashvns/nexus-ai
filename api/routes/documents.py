import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
    status,
)

from core.logger import app_logger
from rag.pipeline import rag_pipeline


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("temp/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
) -> dict:
    file_path: Path | None = None

    try:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are supported",
            )

        file_id = str(uuid4())

        file_path = UPLOAD_DIR / (
            f"{file_id}.pdf"
        )

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        chunk_count = rag_pipeline.ingest_pdf(
            str(file_path)
        )

        app_logger.success(
            f"Document ingested: {file.filename}"
        )

        return {
            "success": True,
            "document_id": file_id,
            "filename": file.filename,
            "chunk_count": chunk_count,
        }

    except HTTPException:
        raise

    except Exception as error:
        app_logger.exception(
            f"Document Upload Error: {error}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document ingestion failed",
        ) from error

    finally:
        if file_path and file_path.exists():
            file_path.unlink()