"""Pydantic models for API request/response schemas."""

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question", min_length=1)
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve")


class SourceResponse(BaseModel):
    document: str
    page: int | None = None
    chunk_text: str
    relevance_score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]
    model: str
    mode: str


class DocumentInfo(BaseModel):
    filename: str
    file_type: str
    chunks: int


class UploadResponse(BaseModel):
    message: str
    files_processed: int
    chunks_created: int
    chunks_stored: int


class StatsResponse(BaseModel):
    collection: str
    total_chunks: int
    storage_path: str


class HealthResponse(BaseModel):
    status: str
    version: str
    mode: str
