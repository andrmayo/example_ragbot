# Resume RAGbot Backend

Python backend for a RAG-based chatbot that ingests resumes and answers queries
about them.

## Project Structure

```
backend/
├── src/
│   └── resume_ragbot/
│       ├── __init__.py
│       ├── main.py              # FastAPI app entrypoint
│       ├── config.py            # Settings/env vars (pydantic-settings)
│       │
│       ├── api/                 # HTTP layer
│       │   ├── __init__.py
│       │   └── routes.py        # All API endpoints (upload, ask, clear, etc.)
│       │
│       ├── extraction/          # Document parsing
│       │   ├── __init__.py
│       │   ├── base.py          # Extractor interface & ExtractedDocument
│       │   └── extractors.py    # PDF, DOCX, ODT, plaintext extractors
│       │
│       ├── rag/                 # RAG pipeline
│       │   ├── __init__.py
│       │   ├── chunking.py      # Text chunking with overlap
│       │   ├── embedding.py     # Embedding generation (sentence-transformers)
│       │   ├── retriever.py     # FAISS vector search/retrieval
│       │   └── prompts.py       # System prompt and QA prompt builder
│       │
│       └── llm/                 # LLM integration
│           ├── __init__.py      # get_client() factory function
│           ├── base.py          # LLMClient ABC, Message, LLMResponse
│           ├── anthropic_client.py
│           ├── openai_client.py
│           └── google_client.py
│
├── tests/
│   ├── unit/                    # Unit tests (pytest)
│   │   ├── conftest.py          # Fixtures for tests
│   │   ├── test_api_routes.py
│   │   └── test_extraction.py
│   ├── eval/                    # Eval harness (standalone)
│   │   ├── __init__.py
│   │   ├── cases.py             # Test case definitions
│   │   ├── metrics.py           # Scoring functions
│   │   └── runner.py            # Evaluation orchestrator
│   └── fixtures/                # Test resume files
│
├── typings/                     # Custom type stubs
│   └── faiss/
│       └── __init__.pyi         # FAISS type stubs for Pyright
│
├── pyproject.toml
└── README.md
```

## Module Overview

### `api/`

FastAPI routes for the REST API:
- `POST /upload` - Upload a single resume
- `POST /upload_batch` - Upload multiple resumes
- `POST /ask` - Ask a question about uploaded resumes
- `DELETE /clear/{collection}` - Clear a collection
- `DELETE /clear_all` - Clear all collections
- `DELETE /resume/{collection}/{filename}` - Remove a specific resume
- `GET /collections` - List all collections

### `extraction/`

Handles parsing different resume file formats (PDF, DOCX, ODT, plain text) into
raw text. All extractors implement the `Extractor` interface defined in `base.py`.

### `rag/`

Core RAG pipeline components:

- **chunking.py** - Splits extracted text into overlapping chunks
- **embedding.py** - Generates L2-normalized vector embeddings
- **retriever.py** - FAISS-based vector search and retrieval
- **prompts.py** - System prompt and QA prompt with source attribution

The vector similarity search engine is FAISS (faiss-cpu). Embeddings are from
sentence-transformers (all-MiniLM-L6-v2 by default), which avoids API costs.

### `llm/`

Abstraction layer for LLM API calls. Supports multiple providers:
- Anthropic (Claude)
- OpenAI (GPT)
- Google (Gemini)

The `get_client()` factory function returns the appropriate client based on
configuration.

### `eval/`

Standalone evaluation harness for measuring RAG quality. Run with:
```bash
python -m tests.eval.runner
```

Measures source recall (did we retrieve the right documents?) and keyword recall
(does the answer contain expected information?).

## Setup

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv sync
```

## Running

```bash
uvicorn resume_ragbot.main:app --reload
```
