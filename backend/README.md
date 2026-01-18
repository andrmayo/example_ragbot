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
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   ├── chat.py      # Chat/query endpoints
│       │   │   └── documents.py # Resume upload endpoints
│       │   └── deps.py          # Dependency injection
│       │
│       ├── extraction/          # Document parsing
│       │   ├── __init__.py
│       │   ├── base.py          # Extractor interface
│       │   ├── docx.py          # .docx extraction
│       │   ├── pdf.py           # PDF extraction
│       │   └── plaintext.py     # .txt extraction
│       │
│       ├── rag/                 # RAG pipeline
│       │   ├── __init__.py
│       │   ├── chunking.py      # Text chunking strategies
│       │   ├── embeddings.py    # Embedding generation
│       │   ├── retriever.py     # Vector search/retrieval
│       │   └── prompts.py       # Prompt templates
│       │
│       ├── llm/                 # LLM integration
│       │   ├── __init__.py
│       │   ├── client.py        # API client wrapper
│       │   └── models.py        # Request/response models
│       │
│       ├── storage/             # Persistence
│       │   ├── __init__.py
│       │   ├── vector_store.py  # Vector DB interface
│       │   └── document_store.py# Raw document storage
│       │
│       └── models/              # Domain models (Pydantic)
│           ├── __init__.py
│           ├── document.py
│           ├── chunk.py
│           └── chat.py
│
├── tests/
│   ├── conftest.py
│   ├── test_extraction/
│   ├── test_rag/
│   └── eval/                    # Eval harness
│       ├── __init__.py
│       ├── datasets/            # Test Q&A pairs
│       └── runner.py            # Evaluation orchestrator
│
├── pyproject.toml
└── README.md
```

## Module Overview

### `extraction/`

Handles parsing different resume file formats (PDF, DOCX, plain text) into raw
text. Each extractor implements a common interface for consistency.

### `rag/`

Core RAG pipeline components:

- **chunking.py** - Splits extracted text into chunks for embedding
- **embeddings.py** - Generates vector embeddings for chunks
- **retriever.py** - Finds relevant chunks for a given query
- **prompts.py** - Prompt templates for the LLM

The vector similarity search engine here is FAISS. FAISS is generally pretty
adaptable, fast, and scalable, while ultimately simpler than engines suitable
for very large scale applications like Chroma and Pinecode. The embeddings are
from sentence-transformers, which should be sufficient while avoiding API costs.
Unless GPU support becomes necessary, we can use faiss-cpu for a lighter
dependency.

### `llm/`

Abstraction layer for LLM API calls. Keeps provider-specific logic isolated so
you can swap between OpenAI, Anthropic, or local models.

### `storage/`

Persistence layer for documents and vectors. Abstracts the vector database so
you can swap implementations (ChromaDB, Qdrant, etc.).

### `eval/`

Evaluation harness for measuring RAG quality. Runs test Q&A pairs through the
pipeline and scores responses to catch regressions.

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
