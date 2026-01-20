import numpy as np
from sentence_transformers import SentenceTransformer

from resume_ragbot.config import settings


class Embedder:
    dimension: int

    def __init__(self, model_name: str = settings.default_embedding_model):
        self.model = SentenceTransformer(model_name)
        dimension = self.model.get_sentence_embedding_dimension()
        if dimension is None:
            raise ValueError(f"Model {model_name} does not support embeddings")
        self.dimension = dimension

    def embed(self, text: str) -> np.ndarray:
        """Embed a single text string."""
        return self.model.encode(text, normalize_embeddings=True, convert_to_numpy=True)

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """Embed multiple texts at once."""
        return self.model.encode(
            texts, normalize_embeddings=True, convert_to_numpy=True
        )
