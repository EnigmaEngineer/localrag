"""FastAPI application entry point."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from localrag import __version__
from localrag.config import settings
from localrag.api.routes import documents, query, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    logger.info(f"Starting LocalRAG v{__version__} | mode={settings.mode.value}")
    yield
    logger.info("Shutting down LocalRAG")


app = FastAPI(
    title="LocalRAG",
    description="Privacy-first document intelligence. Your data never leaves your machine.",
    version=__version__,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(query.router, prefix="/api/v1", tags=["Query"])


if __name__ == "__main__":
    uvicorn.run(
        "localrag.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
