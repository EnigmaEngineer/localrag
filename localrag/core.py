"""Core LocalRAG orchestrator — ties together ingestion, retrieval, and generation."""

from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from localrag.config import LLMMode, Settings, settings
from localrag.ingestion.pipeline import IngestionPipeline
from localrag.retrieval.engine import RetrievalEngine
from localrag.llm.factory import create_llm_client


@dataclass
class Source:
    """A source reference for an answer."""

    document: str
    page: int | None
    chunk_text: str
    relevance_score: float


@dataclass
class Answer:
    """A response from LocalRAG with source citations."""

    text: str
    sources: list[Source] = field(default_factory=list)
    model: str = ""
    mode: str = ""


class LocalRAG:
    """Main entry point for LocalRAG.

    Usage:
        rag = LocalRAG(mode="local")
        rag.ingest("./documents/")
        answer = rag.query("What are the key terms?")
    """

    def __init__(self, mode: str | None = None, **kwargs):
        """Initialize LocalRAG.

        Args:
            mode: "local" for Ollama, "cloud" for OpenAI/Anthropic.
                  Defaults to settings from .env.
            **kwargs: Override any Settings field.
        """
        config_overrides = {}
        if mode:
            config_overrides["mode"] = LLMMode(mode)
        config_overrides.update(kwargs)

        self.settings = Settings(**config_overrides) if config_overrides else settings

        if self.settings.mode == LLMMode.CLOUD:
            self.settings.validate_cloud_mode()

        logger.info(
            f"Initializing LocalRAG | mode={self.settings.mode.value} | "
            f"llm={self.settings.llm_model} | embeddings={self.settings.embed_model}"
        )

        self._ingestion = IngestionPipeline(self.settings)
        self._retrieval = RetrievalEngine(self.settings)
        self._llm = create_llm_client(self.settings)

    def ingest(self, path: str | Path, **kwargs) -> dict:
        """Ingest documents from a file or directory.

        Args:
            path: Path to a single file or directory of documents.

        Returns:
            Summary dict with counts and any errors.
        """
        path = Path(path)
        logger.info(f"Ingesting documents from: {path}")

        if path.is_file():
            documents = self._ingestion.process_file(path)
        elif path.is_dir():
            documents = self._ingestion.process_directory(path)
        else:
            raise FileNotFoundError(f"Path not found: {path}")

        # Store chunks in vector DB
        stored = self._retrieval.add_documents(documents)

        summary = {
            "files_processed": len(set(d.metadata.get("source", "") for d in documents)),
            "chunks_created": len(documents),
            "chunks_stored": stored,
        }
        logger.info(f"Ingestion complete: {summary}")
        return summary

    def query(self, question: str, top_k: int | None = None) -> Answer:
        """Ask a question across all ingested documents.

        Args:
            question: Natural language question.
            top_k: Number of chunks to retrieve (overrides settings).

        Returns:
            Answer with text and source citations.
        """
        k = top_k or self.settings.top_k
        logger.info(f"Query: '{question}' | top_k={k}")

        # Retrieve relevant chunks
        retrieved = self._retrieval.search(question, top_k=k)

        if not retrieved:
            return Answer(
                text="I couldn't find any relevant information in the ingested documents.",
                sources=[],
                model=self.settings.llm_model,
                mode=self.settings.mode.value,
            )

        # Build context from retrieved chunks
        context = "\n\n---\n\n".join(
            f"[Source: {r.metadata.get('source', 'unknown')}, "
            f"Page: {r.metadata.get('page', 'N/A')}]\n{r.page_content}"
            for r in retrieved
        )

        # Generate answer with LLM
        response = self._llm.generate(question=question, context=context)

        # Build source citations
        sources = [
            Source(
                document=r.metadata.get("source", "unknown"),
                page=r.metadata.get("page"),
                chunk_text=r.page_content[:200] + "..."
                if len(r.page_content) > 200
                else r.page_content,
                relevance_score=r.metadata.get("score", 0.0),
            )
            for r in retrieved
        ]

        return Answer(
            text=response,
            sources=sources,
            model=self.settings.llm_model,
            mode=self.settings.mode.value,
        )

    def get_stats(self) -> dict:
        """Return collection statistics."""
        return self._retrieval.get_stats()

    def reset(self) -> None:
        """Delete all ingested documents and reset the vector store."""
        self._retrieval.reset()
        logger.warning("All documents deleted. Vector store reset.")
