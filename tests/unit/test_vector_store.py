from rag.embeddings import embedding_service
from rag.vector_store import vector_store


def main():
    documents = [
        "Nexus AI is a multi-agent AI platform.",
        "FAISS provides fast vector similarity search.",
        "Planner Agent creates execution plans.",
    ]

    embeddings = embedding_service.embed_documents(
        documents
    )

    vector_store.add(
        documents=documents,
        embeddings=embeddings,
    )

    query_embedding = embedding_service.embed_query(
        "What is Nexus AI?"
    )

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=2,
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    main()