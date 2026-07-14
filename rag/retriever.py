from rag.embeddings import embedding_service
from rag.vector_store import vector_store


class Retriever:
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[dict]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = embedding_service.embed_query(
            query
        )

        return vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )


retriever = Retriever()