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

    def clear(self) -> None:
        """Clear the index and chunks."""
        self.index = None
        self.chunks = []

    def remove_source(self, source: str) -> int:
        """
        Remove all chunks from a specific source and returns number removed.
        This is slow because index has to be rebuilt whenever it gets called.
        """
        original_count = len(self.chunks)
        self.chunks = [c for c in self.chunks if c.source != source]
        removed = original_count - len(self.chunks)

        if removed > 0 and self.chunks:
            # Rebuild index
            embeddings = self.embedder.embed_batch([c.text for c in self.chunks])
            self.index = faiss.IndexFlatL2(self.embedder.dimension)
            self.index.add(embeddings)
        elif not self.chunks:
            self.index = None

        return removed
