from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resume_ragbot.api.routes import router

app = FastAPI(
    title="Resume-RAGbot",
    description="RAG-based chatbot for resume Q&A",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
