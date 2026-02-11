"""Embedding function factory — supports local and cloud embeddings."""

from langchain_core.embeddings import Embeddings
from loguru import logger

from localrag.config import LLMMode, Settings


def create_embedding_function(settings: Settings) -> Embeddings:
    """Create the appropriate embedding function based on mode."""
    if settings.mode == LLMMode.LOCAL:
        return _create_ollama_embeddings(settings)
    else:
        return _create_openai_embeddings(settings)


def _create_ollama_embeddings(settings: Settings) -> Embeddings:
    """Create Ollama-based local embeddings."""
    from langchain_community.embeddings import OllamaEmbeddings

    logger.info(f"Using local embeddings: {settings.embed_model}")
    return OllamaEmbeddings(
        model=settings.embed_model,
        base_url=settings.ollama_base_url,
    )


def _create_openai_embeddings(settings: Settings) -> Embeddings:
    """Create OpenAI cloud embeddings."""
    from langchain_openai import OpenAIEmbeddings

    logger.info("Using OpenAI embeddings: text-embedding-3-small")
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.openai_api_key,
    )
