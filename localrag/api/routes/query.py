"""Query endpoint — ask questions across ingested documents."""

from fastapi import APIRouter, HTTPException
from loguru import logger

from localrag.api.models import QueryRequest, QueryResponse, SourceResponse
from localrag.core import LocalRAG

router = APIRouter()

_rag: LocalRAG | None = None


def _get_rag() -> LocalRAG:
    global _rag
    if _rag is None:
        _rag = LocalRAG()
    return _rag


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Ask a question across all ingested documents."""
    try:
        rag = _get_rag()
        answer = rag.query(question=request.question, top_k=request.top_k)

        return QueryResponse(
            answer=answer.text,
            sources=[
                SourceResponse(
                    document=s.document,
                    page=s.page,
                    chunk_text=s.chunk_text,
                    relevance_score=s.relevance_score,
                )
                for s in answer.sources
            ],
            model=answer.model,
            mode=answer.mode,
        )
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
