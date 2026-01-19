# Simple monorepo for chatbot with RAG

## Project

A fullstack chatbot that ingests resumes in doc, docx, pdf, or plain text format
and uses an LLM and RAG to answer queries an LLM about the resume.

## Goals

- Backend robust to different file types
- RAG pipeline structured to provide context from resumes to the LLM to reduce
  hallucinations.
- Eval harness
- User-friendly frontend

## Implementation

- backend: located in ./backend/. RAG is implemented directly without very high
  level tools like LangChain (for now). The main focus is the Python backend,
  which is ./backend/ and uses src layout, and to get extraction, LLM api-calls,
  and RAG working for resumes in pdf format. More info in backend/README.md.
- frontend: located in ./frontend/. Will be a React frontend using TypeScript.
  CSS is managed with Tailwind.

## Bash commands

source backend/.venv/bin/activate: Activate venv (created with uv) for Python
backend

## Style

Never (or almost never) use comments to tell Pyright to ignore type issues.
