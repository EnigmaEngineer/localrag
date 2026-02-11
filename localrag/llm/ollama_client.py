"""Ollama client for local LLM inference."""

import ollama as ollama_sdk
from loguru import logger

from localrag.config import Settings
from localrag.llm.base import BaseLLMClient
from localrag.llm.prompts import RAG_SYSTEM_PROMPT, format_rag_prompt


class OllamaClient(BaseLLMClient):
    """Local LLM inference via Ollama."""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.model = settings.llm_model
        self.client = ollama_sdk.Client(host=settings.ollama_base_url)
        logger.info(f"OllamaClient initialized | model={self.model}")

    def generate(self, question: str, context: str) -> str:
        """Generate answer using local Ollama model."""
        user_prompt = format_rag_prompt(question=question, context=context)

        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            options={
                "temperature": self.settings.temperature,
                "num_predict": self.settings.max_tokens,
            },
        )

        return response["message"]["content"]
