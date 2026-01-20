# RAG Chatbot for Resume Queries

This is a chatbot web application that uses retrieval augmented generation (RAG)
to read resumes and response to questions about them.

## Supported document types

This has been tested most thoroughly with files in pdf format, but it should
also work for .pdf, .odt, and .txt (plain text) files.

## Usage

If one resume is uploaded, the chatbot can answer general questions about it. If
several resumes are uploaded, it can also answer questions to select which
resume or resumes best match specified criteria, e.g. which candidates have a
given skill. Currently, it's only set up to do this for a small number of
resumes, and may not answer comprehensively for number of resumes > 20.

## Implementation

The backend was built in Python with Uvicorn for the ASGI server and FastAPI for
the API. The backend was build in TypeScript with the React library, as well as
Tailwind to handle CSS and Vite as a build tool and development server. The
application as a whole works as a static site with RPC architecture.

On the backend, configuration is controlled by a combination of environment
variables and `config.py`. These include the LLM provider, which is Anthropic by
default but can be changed to OpenAI or Google (Gemini) as long as an API key is
present as an environment variable. The number of chunks that get retrieved for
RAG is also controlled in `config.py`.

The actual vector embeddings come from the sentence-transformers Python library.
The specific sentence-transformers embedding to use is also controlled in
`config.py`. Indexing and search over chunk embeddings is done with the FAISS
library in Python. The L2 norm is used for retrieval of the top-k chunks via a
brute force search, which should work fine even for a few thousand resumes. To
scale beyond perhaps a 100000, some combination of GPU operations, vector
compression, and a more efficient search algorithm (e.g. k-means clustering)
would probably be necessary.

## Testing

Tests for the backend, including pytest unit tests and an eval runner, are in
`backend/tests/`. The frontend is easiest to test and debug using a Vite
development server by running `npm run dev` from the `frontend` dir.
