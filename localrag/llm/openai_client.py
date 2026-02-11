"""OpenAI client for cloud LLM inference."""

from openai import OpenAI
from loguru import logger

from localrag.config import Settings
from localrag.llm.base import BaseLLMClient
from localrag.llm.prompts import RAG_SYSTEM_PROMPT, format_rag_prompt


class OpenAIClient(BaseLLMClient):
    """Cloud LLM inference via OpenAI API."""

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.model = settings.llm_model if settings.llm_model != "llama3.2" else "gpt-4o-mini"
        self.client = OpenAI(api_key=settings.openai_api_key)
        logger.info(f"OpenAIClient initialized | model={self.model}")

    def generate(self, question: str, context: str) -> str:
        """Generate answer using OpenAI API."""
        user_prompt = format_rag_prompt(question=question, context=context)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=self.settings.temperature,
            max_tokens=self.settings.max_tokens,
        )

        return response.choices[0].message.content
