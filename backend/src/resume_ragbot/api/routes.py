from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from resume_ragbot.config import LLMProvider
from resume_ragbot.extraction.extractors import EXTRACTORS
from resume_ragbot.llm import get_client
from resume_ragbot.llm.base import Message
from resume_ragbot.rag.chunking import chunk_text
from resume_ragbot.rag.prompts import SYSTEM_PROMPT, build_qa_prompt
from resume_ragbot.rag.retriever import Retriever

router = APIRouter()

retriever = Retriever()


class QuestionRequest(BaseModel):
    question: str
    provider: LLMProvider | None = None
    model: str | None = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, str]:
    """Upload a resum file and index it for Q&A."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_path = Path(file.filename)

    extractor = None
    for ext in EXTRACTORS:
        if ext.supports(file_path):
            extractor = ext
            break

    if extractor is None:
        raise HTTPException(
            status_code=400, detail=f"Unsupported file type: {file_path.suffix}"
        )

    with NamedTemporaryFile(suffix=file_path.suffix, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()
        document = extractor.extract(Path(tmp.name))

    chunks = chunk_text(document.content, source=file.filename)
    retriever.add_chunks(chunks)

    return {"message": f"Indexed {len(chunks)} chunks from {file.filename}"}


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """Ask a question about uploaded resumes."""
    relevant_chunks = retriever.search(request.question, k=3)

    if not relevant_chunks:
        return AnswerResponse(
            answer="No resume content has been uploaded yet.", sources=[]
        )

    context = [c.text for c in relevant_chunks]
    sources = list(set(c.source for c in relevant_chunks))

    prompt = build_qa_prompt(request.question, context)

    client = get_client(provider=request.provider, model=request.model)
    response = client.complete(
        messages=[Message(role="user", content=prompt)],
        system=SYSTEM_PROMPT,
    )

    return AnswerResponse(answer=response.content, sources=sources)
