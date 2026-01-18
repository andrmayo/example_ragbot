from fastapi import FastAPI

from resume_ragbot.api.routes import router

app = FastAPI(
    title="Resume-RAGbot",
    description="RAG-based chatbot for resume Q&A",
    version="0.1.0",
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
