from rag.embeddings import embedding_service
from rag.retriever import retriever
from rag.vector_store import vector_store


def main():
    documents = [
        "Nexus AI is a multi-agent AI platform.",
        "FAISS provides vector similarity search.",
        "Planner Agent creates execution plans.",
    ]

    embeddings = embedding_service.embed_documents(
        documents
    )

    vector_store.add(
        documents=documents,
        embeddings=embeddings,
    )

    results = retriever.retrieve(
        query="What does Planner Agent do?",
        top_k=2,
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    main()