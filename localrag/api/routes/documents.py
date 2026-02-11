"""Document upload and management endpoints."""

import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from loguru import logger

from localrag.api.models import StatsResponse, UploadResponse
from localrag.config import settings
from localrag.core import LocalRAG

router = APIRouter()

# Lazy-initialized RAG instance
_rag: LocalRAG | None = None


def _get_rag() -> LocalRAG:
    global _rag
    if _rag is None:
        _rag = LocalRAG()
    return _rag


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile):
    """Upload and ingest a document."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Save uploaded file
    upload_dir = settings.upload_path
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.filename

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        logger.info(f"Uploaded: {file.filename}")

        # Ingest the document
        rag = _get_rag()
        result = rag.ingest(file_path)

        return UploadResponse(
            message=f"Successfully ingested {file.filename}",
            **result,
        )
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get collection statistics."""
    rag = _get_rag()
    return StatsResponse(**rag.get_stats())
