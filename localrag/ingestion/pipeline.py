"""Document ingestion pipeline — parse, chunk, and prepare documents for indexing."""

from pathlib import Path

from langchain_core.documents import Document
from loguru import logger

from localrag.config import Settings
from localrag.ingestion.parsers import parse_file
from localrag.ingestion.chunker import SemanticChunker


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv"}


class IngestionPipeline:
    """Orchestrates document parsing and chunking."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.chunker = SemanticChunker(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def process_file(self, file_path: Path) -> list[Document]:
        """Process a single file into chunked documents."""
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return []

        logger.info(f"Parsing: {file_path.name}")
        raw_docs = parse_file(file_path)

        chunks = self.chunker.split(raw_docs)
        logger.info(f"  → {len(raw_docs)} pages → {len(chunks)} chunks")

        return chunks

    def process_directory(self, dir_path: Path) -> list[Document]:
        """Process all supported files in a directory."""
        all_chunks = []
        files = [
            f for f in dir_path.rglob("*")
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        logger.info(f"Found {len(files)} supported files in {dir_path}")

        for file_path in sorted(files):
            chunks = self.process_file(file_path)
            all_chunks.extend(chunks)

        return all_chunks
