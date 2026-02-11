"""Application configuration using pydantic-settings."""

from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMMode(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"


class Settings(BaseSettings):
    """LocalRAG configuration.

    All settings can be overridden via environment variables
    prefixed with LOCALRAG_ (e.g., LOCALRAG_MODE=cloud).
    """

    model_config = SettingsConfigDict(
        env_prefix="LOCALRAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Mode
    mode: LLMMode = LLMMode.LOCAL

    # LLM settings
    llm_model: str = "llama3.2"
    embed_model: str = "nomic-embed-text"
    temperature: float = 0.1
    max_tokens: int = 1024

    # Cloud API keys (only needed in cloud mode)
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Retrieval
    top_k: int = 5
    use_hybrid_search: bool = True
    use_reranker: bool = False

    # Storage
    chroma_path: Path = Path("./data/chroma")
    upload_path: Path = Path("./data/uploads")
    collection_name: str = "localrag_docs"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    cors_origins: list[str] = ["*"]

    # Ollama
    ollama_base_url: str = "http://localhost:11434"

    def validate_cloud_mode(self) -> None:
        """Ensure API keys are set when using cloud mode."""
        if self.mode == LLMMode.CLOUD and not self.openai_api_key:
            raise ValueError(
                "LOCALRAG_OPENAI_API_KEY is required when LOCALRAG_MODE=cloud"
            )


settings = Settings()
