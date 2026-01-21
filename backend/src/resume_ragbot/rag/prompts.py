from resume_ragbot.rag.chunking import Chunk

SYSTEM_PROMPT = """You are a helpful assistant that answers questions about resumes.
You will be given relevant excerpts from one or more resumes and a question.
Answer based on the provided context. If the information is not in the context, say so.
Be concise and direct.

You must respond with valid JSON in the following format:
{"answer": "<your answer here>", "sources_used": ["<filename1>", "<filename2>"]}

The sources_used array must contain the exact filenames (e.g., "alice_resume.pdf") of the resumes you actually used to answer the question. Only include sources that directly contributed to your answer. If no sources were relevant, use an empty array."""


def build_qa_prompt(question: str, context_chunks: list[Chunk]) -> str:
    """Build a prompt for question answering over resume chunks."""
    context_parts = [f"[From {c.source}]: {c.text}" for c in context_chunks]
    context = "\n\n".join(context_parts)
    return f"""Context from resumes:

    {context}

    ---

    Question: {question}

    Answer:"""
