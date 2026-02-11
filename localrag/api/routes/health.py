"""Health check endpoint."""

from fastapi import APIRouter

from localrag import __version__
from localrag.api.models import HealthResponse
from localrag.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and configuration."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        mode=settings.mode.value,
    )
