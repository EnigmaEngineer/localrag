"""Tests for LocalRAG configuration."""

import pytest

from localrag.config import LLMMode, Settings


class TestSettings:
    """Test configuration management."""

    def test_default_mode_is_local(self):
        s = Settings()
        assert s.mode == LLMMode.LOCAL

    def test_default_chunk_size(self):
        s = Settings()
        assert s.chunk_size == 512
        assert s.chunk_overlap == 50

    def test_default_retrieval_settings(self):
        s = Settings()
        assert s.top_k == 5
        assert s.use_hybrid_search is True

    def test_cloud_mode_requires_api_key(self):
        s = Settings(mode=LLMMode.CLOUD)
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            s.validate_cloud_mode()

    def test_cloud_mode_with_api_key(self):
        s = Settings(mode=LLMMode.CLOUD, openai_api_key="sk-test-123")
        s.validate_cloud_mode()  # Should not raise

    def test_override_settings(self):
        s = Settings(chunk_size=1024, top_k=10)
        assert s.chunk_size == 1024
        assert s.top_k == 10
