import numpy as np
import faiss

from resume_ragbot.rag.chunking import Chunk
from resume_ragbot.rag.embedding import Embedder


class Retriever:
    def __init__(self, embedder: Embedder | None = None):
        self.embedder = embedder or Embedder()
        self.index: faiss.IndexFlatL2 | None = None
        self.chunks: list[Chunk] = []

    def add_chunks(self, chunks: list[Chunk]) -> None:
        """Add chunks to the index."""
        if not chunks:
            return

        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_batch(texts)

        if self.index is None:
            self.index = faiss.IndexFlatL2(self.embedder.dimension)

        self.index.add(embeddings)
        self.chunks.extend(chunks)

    def search(self, query: str, k: int = 3) -> list[Chunk]:
        """Find the k most similar chunks to the query."""
        if self.index is None or len(self.chunks) == 0:
            return []

        query_embedding = self.embedder.embed(query)
        query_embedding = np.expand_dims(query_embedding, axis=0)

        k = min(k, len(self.chunks))
        _, indices = self.index.search(query_embedding, k)

        return [self.chunks[i] for i in indices[0]]
