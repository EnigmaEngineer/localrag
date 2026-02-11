<p align="center">
  <img src="docs/assets/localrag-banner.png" alt="LocalRAG" width="600"/>
</p>

<h1 align="center">LocalRAG</h1>

<p align="center">
  <strong>Privacy-first document intelligence. Your data never leaves your machine.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#api-reference">API</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"/>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"/>
  <img src="https://img.shields.io/badge/build%20in%20public-🔨-orange?style=flat-square" alt="Build in Public"/>
</p>

---

## The Problem

Most RAG (Retrieval-Augmented Generation) solutions send your documents to third-party cloud services. For sensitive data — legal contracts, medical records, financial reports — that's a non-starter.

**LocalRAG** is a privacy-first document Q&A system that processes everything locally by default, with optional cloud LLM integration when privacy requirements allow it.

Upload documents → Ask questions → Get cited answers. **No data leaves your machine unless you explicitly choose cloud mode.**

## Features

- 🔒 **Privacy-first** — All document processing, chunking, and embedding happens locally
- 📄 **Multi-format ingestion** — PDF, DOCX, TXT, Markdown, CSV support
- 🔍 **Hybrid search** — Combines semantic (vector) + keyword (BM25) retrieval for better accuracy
- 🧠 **Flexible LLM backend** — Use Ollama (local) or OpenAI/Anthropic (cloud) — your choice
- 📊 **Source citations** — Every answer includes references to specific document chunks
- ⚡ **FastAPI backend** — Production-ready REST API with async support
- 📈 **Built-in evaluation** — Measure retrieval accuracy and answer quality with RAGAS
- 🐳 **Docker ready** — One command to run the entire stack

## Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) (for local LLM mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/localrag.git
cd localrag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull a local model (optional, for fully local mode)
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Run LocalRAG

```bash
# Start the API server
python -m localrag.api.main

# Server runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Basic Usage

```python
from localrag import LocalRAG

# Initialize with local mode (default)
rag = LocalRAG(mode="local")

# Ingest documents
rag.ingest("./documents/")

# Ask questions
answer = rag.query("What are the key terms in the contract?")
print(answer.text)
print(answer.sources)  # Document chunks with page numbers
```

### API Usage

```bash
# Upload a document
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@contract.pdf"

# Query your documents
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the payment terms?", "top_k": 5}'
```

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      FastAPI Server                       │
│                   (REST API + WebSocket)                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Ingestion   │  │  Retrieval   │  │  Generation    │  │
│  │  Pipeline    │  │  Engine      │  │  Layer         │  │
│  │             │  │              │  │                │  │
│  │ • PDF Parse │  │ • Semantic   │  │ • Ollama       │  │
│  │ • DOCX Parse│  │ • BM25       │  │ • OpenAI       │  │
│  │ • Chunking  │  │ • Hybrid     │  │ • Anthropic    │  │
│  │ • Cleaning  │  │ • Re-ranking │  │ • Prompt Mgmt  │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                   │           │
│         ▼                ▼                   ▼           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              ChromaDB (Vector Store)                 │ │
│  │           Local persistent storage                  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │           Evaluation Module (RAGAS)                 │ │
│  │    Retrieval accuracy • Answer quality • Faithfulness│ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## Project Structure

```
localrag/
├── localrag/                  # Core package
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── ingestion/             # Document processing pipeline
│   │   ├── __init__.py
│   │   ├── parsers.py         # PDF, DOCX, TXT parsers
│   │   ├── chunker.py         # Semantic chunking strategies
│   │   └── preprocessor.py    # Text cleaning & normalization
│   ├── retrieval/             # Search & retrieval
│   │   ├── __init__.py
│   │   ├── vectorstore.py     # ChromaDB integration
│   │   ├── bm25.py            # Keyword search
│   │   ├── hybrid.py          # Hybrid search orchestration
│   │   └── reranker.py        # Cross-encoder re-ranking
│   ├── llm/                   # LLM abstraction layer
│   │   ├── __init__.py
│   │   ├── base.py            # Base LLM interface
│   │   ├── ollama_client.py   # Local inference via Ollama
│   │   ├── openai_client.py   # OpenAI API client
│   │   └── prompts.py         # Prompt templates
│   ├── api/                   # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py            # App entry point
│   │   ├── routes/            # API route handlers
│   │   │   ├── documents.py
│   │   │   ├── query.py
│   │   │   └── health.py
│   │   └── models.py          # Pydantic request/response models
│   ├── evaluation/            # Quality measurement
│   │   ├── __init__.py
│   │   └── metrics.py         # RAGAS integration
│   └── utils/                 # Shared utilities
│       ├── __init__.py
│       └── logging.py
├── tests/                     # Test suite
│   ├── unit/
│   └── integration/
├── docs/                      # Documentation
│   ├── architecture/
│   └── guides/
├── scripts/                   # Helper scripts
│   └── seed_data.py
├── docker/                    # Docker configuration
│   └── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Makefile
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/documents/upload` | Upload and ingest a document |
| `GET` | `/api/v1/documents` | List all ingested documents |
| `DELETE` | `/api/v1/documents/{id}` | Remove a document |
| `POST` | `/api/v1/query` | Ask a question across your documents |
| `POST` | `/api/v1/query/stream` | Stream a response (SSE) |
| `GET` | `/api/v1/health` | Health check |
| `GET` | `/api/v1/stats` | Collection statistics |

## Configuration

LocalRAG uses environment variables for configuration. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `LOCALRAG_MODE` | `local` | `local` (Ollama) or `cloud` (OpenAI/Anthropic) |
| `LOCALRAG_LLM_MODEL` | `llama3.2` | Model name for generation |
| `LOCALRAG_EMBED_MODEL` | `nomic-embed-text` | Model for embeddings |
| `LOCALRAG_CHUNK_SIZE` | `512` | Token count per chunk |
| `LOCALRAG_CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `LOCALRAG_TOP_K` | `5` | Number of chunks to retrieve |
| `LOCALRAG_CHROMA_PATH` | `./data/chroma` | ChromaDB storage path |
| `OPENAI_API_KEY` | — | Required only for cloud mode |

## Roadmap

### Phase 1: Core (Weeks 1-4) ← **Current**
- [x] Project structure & configuration
- [ ] Document ingestion pipeline (PDF, DOCX, TXT)
- [ ] Semantic chunking with overlap
- [ ] ChromaDB vector store integration
- [ ] Basic RAG query pipeline
- [ ] FastAPI REST endpoints
- [ ] Ollama integration for local inference

### Phase 2: Production-Grade (Weeks 5-8)
- [ ] Hybrid search (semantic + BM25)
- [ ] Cross-encoder re-ranking
- [ ] Streaming responses (SSE)
- [ ] Docker containerization
- [ ] RAGAS evaluation pipeline
- [ ] Multi-modal support (tables, images from PDFs)

### Phase 3: Enterprise Features (Weeks 9-12)
- [ ] LangChain agent integration
- [ ] Multi-tenancy support
- [ ] Authentication & audit logging
- [ ] Async document processing queue
- [ ] Comprehensive benchmarks vs. cloud RAG solutions
- [ ] CLI tool for terminal-based Q&A

## Performance

> Benchmarks coming in Phase 2. Will compare retrieval accuracy, latency, and answer quality against cloud-based RAG solutions.

## Built With

- **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance async API framework
- **[LangChain](https://python.langchain.com/)** — LLM orchestration and chain management
- **[ChromaDB](https://www.trychroma.com/)** — Open-source vector database
- **[Ollama](https://ollama.ai/)** — Local LLM inference
- **[RAGAS](https://docs.ragas.io/)** — RAG evaluation framework

## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) before submitting a PR.

```bash
# Setup development environment
pip install -r requirements-dev.txt
pre-commit install

# Run tests
make test

# Run linting
make lint
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Building this in public.</strong> Follow along on <a href="https://linkedin.com/in/yourprofile">LinkedIn</a> for daily updates.
</p>
