"""Tests for document parsers."""

import tempfile
from pathlib import Path

from localrag.ingestion.parsers import parse_file


class TestTextParser:
    """Test plain text file parsing."""

    def test_parse_txt_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello, this is a test document.\nIt has two lines.")
            f.flush()

            docs = parse_file(Path(f.name))
            assert len(docs) == 1
            assert "Hello" in docs[0].page_content
            assert docs[0].metadata["file_type"] == "txt"

    def test_parse_md_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Title\n\nSome markdown content.")
            f.flush()

            docs = parse_file(Path(f.name))
            assert len(docs) == 1
            assert "# Title" in docs[0].page_content
            assert docs[0].metadata["file_type"] == "md"


class TestCSVParser:
    """Test CSV file parsing."""

    def test_parse_csv_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age,city\nAlice,30,NYC\nBob,25,LA\n")
            f.flush()

            docs = parse_file(Path(f.name))
            assert len(docs) == 2
            assert "Alice" in docs[0].page_content
            assert docs[0].metadata["row"] == 1
