"""Semantic chunking strategies for document splitting."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SemanticChunker:
    """Split documents into semantically meaningful chunks.

    Uses recursive character splitting with configurable size and overlap,
    prioritizing natural language boundaries (paragraphs > sentences > words).
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""],
            length_function=len,
            is_separator_regex=False,
        )

    def split(self, documents: list[Document]) -> list[Document]:
        """Split a list of documents into chunks, preserving metadata."""
        chunks = self.splitter.split_documents(documents)

        # Add chunk index to metadata
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_index"] = i

        return chunks
