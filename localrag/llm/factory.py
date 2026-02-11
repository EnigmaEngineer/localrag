"""LLM client factory — creates the right client based on configuration."""

from localrag.config import LLMMode, Settings
from localrag.llm.base import BaseLLMClient
from localrag.llm.ollama_client import OllamaClient
from localrag.llm.openai_client import OpenAIClient


def create_llm_client(settings: Settings) -> BaseLLMClient:
    """Create an LLM client based on the configured mode."""
    if settings.mode == LLMMode.LOCAL:
        return OllamaClient(settings)
    else:
        return OpenAIClient(settings)
