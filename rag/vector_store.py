import faiss
import numpy as np

from core.logger import app_logger


class FAISSVectorStore:
    def __init__(self):
        self.index: faiss.Index | None = None
        self.documents: list[str] = []

    def add(
        self,
        documents: list[str],
        embeddings: np.ndarray,
    ) -> None:
        if not documents:
            raise ValueError("Documents cannot be empty")

        if len(documents) != len(embeddings):
            raise ValueError(
                "Documents and embeddings count must match"
            )

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32,
        )

        dimension = embeddings.shape[1]

        if self.index is None:
            self.index = faiss.IndexFlatIP(dimension)

        if self.index.d != dimension:
            raise ValueError(
                "Embedding dimension does not match FAISS index"
            )

        self.index.add(embeddings)
        self.documents.extend(documents)

        app_logger.success(
            f"Added {len(documents)} documents to FAISS"
        )

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ) -> list[dict]:
        if self.index is None or self.index.ntotal == 0:
            return []

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32,
        )

        top_k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(
            query_embedding,
            top_k,
        )

        results: list[dict] = []

        for score, index in zip(scores[0], indices[0]):
            results.append(
                {
                    "content": self.documents[index],
                    "score": float(score),
                }
            )

        return results


vector_store = FAISSVectorStore()