from collections import defaultdict
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

retrievers: dict[str, Retriever] = defaultdict(Retriever)


class QuestionRequest(BaseModel):
    question: str
    provider: LLMProvider | None = None
    model: str | None = None
    collection: str = "default"


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...), collection: str = "default"
) -> dict[str, str]:
    """
    Upload a resum file and index it for Q&A.
    Optionally pass a collection name, default collection is 'default'.
    """
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
    retrievers[collection].add_chunks(chunks)

    return {
        "message": f"Indexed {len(chunks)} chunks from '{file.filename}' into '{collection}'"
    }


@router.post("/upload_batch")
async def upload_resumes(
    files: list[UploadFile] = File(...), collection: str = "default"
) -> dict[str, object]:
    """
    Upload multiple resume files and index them for Q&A.
    Skips unsupported file types and reprots results.
    """
    results: dict[str, str] = {}
    total_chunks = 0

    for file in files:
        if not file.filename:
            continue

        file_path = Path(file.filename)

        extractor = None

        for ext in EXTRACTORS:
            if ext.supports(file_path):
                extractor = ext
                break

        if extractor is None:
            results[file.filename] = f"skipped (unsupported type: {file_path.suffix})"
            continue

        with NamedTemporaryFile(suffix=file_path.suffix, delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()
            document = extractor.extract(Path(tmp.name))

        chunks = chunk_text(document.content, source=file.filename)
        retrievers[collection].add_chunks(chunks)
        total_chunks += len(chunks)
        results[file.filename] = f"indexed {len(chunks)} chunks"

    return {
        "message": f"Indexed {total_chunks} total chunks into '{collection}'",
        "files": results,
    }


@router.post("/ask")
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """Ask a question about uploaded resumes."""
    relevant_chunks = retrievers[request.collection].search(request.question, k=3)

    if not relevant_chunks:
        return AnswerResponse(
            answer="No resume content has been uploaded yet.", sources=[]
        )

    sources = list(set(c.source for c in relevant_chunks))

    prompt = build_qa_prompt(request.question, relevant_chunks)

    client = get_client(provider=request.provider, model=request.model)
    response = client.complete(
        messages=[Message(role="user", content=prompt)],
        system=SYSTEM_PROMPT,
    )

    return AnswerResponse(answer=response.content, sources=sources)


@router.delete("/clear/{collection}")
def clear_index(collection: str) -> dict[str, str]:
    """Clear indexes for a collection of resumes."""
    if collection in retrievers:
        retrievers[collection].clear()
        del retrievers[collection]
    return {"message": f"Collection '{collection}' cleared"}


@router.delete("/clear_all")
def clear_all() -> dict[str, str]:
    """Clear all indexes for all collections of resumes."""
    n_collections = len(retrievers)
    n_chunk = sum(len(ret.chunks) for ret in retrievers.values())
    retrievers.clear()
    return {"message": f"Cleared {n_chunk} chunks from {n_collections}"}


@router.get("/collections")
async def list_collections() -> dict[str, list[str]]:
    return {"collections": list(retrievers.keys())}


@router.delete("/resume/{collection}/{filename}")
def remove_resume(collection: str, filename: str) -> dict[str, str]:
    """Remove a specific resume from a collection or all collections (*)."""
    # if collection == "*", remove resume from all collections
    if collection == "*":
        removed = 0
        for coll in retrievers.values():
            removed += coll.remove_source(filename)
        if removed == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Resume '{filename}' not found in any collection",
            )
        return {
            "message": f"Removed {removed} chunks from '{filename}' for all collections"
        }

    if collection not in retrievers:
        raise HTTPException(
            status_code=404, detail=f"Collection '{collection}' not found"
        )

    removed = retrievers[collection].remove_source(filename)
    if removed == 0:
        raise HTTPException(status_code=404, detail=f"Resume '{filename}' not found")

    return {"message": f"Removed {removed} chunks from '{filename}' for {collection}"}
