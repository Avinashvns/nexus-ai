import numpy as np
from sentence_transformers import SentenceTransformer

from core.logger import app_logger


class EmbeddingService:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ):
        app_logger.info(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(model_name)

        app_logger.success(
            "Embedding model loaded successfully"
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> np.ndarray:
        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings.astype(np.float32)

    def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.astype(np.float32)


embedding_service = EmbeddingService()