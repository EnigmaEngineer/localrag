"""Retrieval engine — vector search, BM25, and hybrid retrieval."""

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from loguru import logger

from localrag.config import LLMMode, Settings
from localrag.retrieval.embeddings import create_embedding_function


class RetrievalEngine:
    """Manages document storage and retrieval via ChromaDB."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.settings.chroma_path.mkdir(parents=True, exist_ok=True)

        self._embedding_fn = create_embedding_function(settings)

        self._client = chromadb.PersistentClient(
            path=str(settings.chroma_path)
        )

        self._vectorstore = Chroma(
            client=self._client,
            collection_name=settings.collection_name,
            embedding_function=self._embedding_fn,
        )

        logger.info(
            f"RetrievalEngine initialized | collection={settings.collection_name} "
            f"| storage={settings.chroma_path}"
        )

    def add_documents(self, documents: list[Document]) -> int:
        """Add documents to the vector store.

        Returns:
            Number of chunks successfully stored.
        """
        if not documents:
            return 0

        self._vectorstore.add_documents(documents)
        return len(documents)

    def search(self, query: str, top_k: int = 5) -> list[Document]:
        """Search for relevant document chunks.

        Args:
            query: Natural language query.
            top_k: Number of results to return.

        Returns:
            List of relevant Documents with metadata.
        """
        results = self._vectorstore.similarity_search_with_relevance_scores(
            query, k=top_k
        )

        documents = []
        for doc, score in results:
            doc.metadata["score"] = round(score, 4)
            documents.append(doc)

        logger.debug(f"Retrieved {len(documents)} chunks for query: '{query[:50]}...'")
        return documents

    def get_stats(self) -> dict:
        """Return collection statistics."""
        collection = self._client.get_collection(self.settings.collection_name)
        return {
            "collection": self.settings.collection_name,
            "total_chunks": collection.count(),
            "storage_path": str(self.settings.chroma_path),
        }

    def reset(self) -> None:
        """Delete all documents in the collection."""
        self._client.delete_collection(self.settings.collection_name)
        # Recreate empty collection
        self._vectorstore = Chroma(
            client=self._client,
            collection_name=self.settings.collection_name,
            embedding_function=self._embedding_fn,
        )
