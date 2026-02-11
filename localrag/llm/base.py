"""Base interface for LLM clients."""

from abc import ABC, abstractmethod

from localrag.config import Settings


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def generate(self, question: str, context: str) -> str:
        """Generate an answer given a question and retrieved context.

        Args:
            question: The user's question.
            context: Concatenated relevant document chunks.

        Returns:
            Generated answer string.
        """
        ...
