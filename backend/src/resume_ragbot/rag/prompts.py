SYSTEM_PROMPT = """You are a helpful assistant that answers questions about resumes.
You will be given relevant excerpts from a resume and a question about it.
Answer based on the provided context. If the information is not in the context, say so.
Be concise and direct."""


def build_qa_prompt(question: str, context_chunks: list[str]) -> str:
    """Build a prompt for question answering over resume chunks."""
    context = "\n\n---\n\n".join(context_chunks)

    return f"""Context from resume:

    {context}

    ---

    Question: {question}

    Answer:"""
