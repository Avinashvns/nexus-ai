from rag.embeddings import embedding_service


def main():
    texts = [
        "Nexus AI is a multi-agent platform.",
        "RAG uses embeddings for semantic search.",
    ]

    document_embeddings = (
        embedding_service.embed_documents(texts)
    )

    query_embedding = embedding_service.embed_query(
        "What is Nexus AI?"
    )

    print(
        "Document Shape:",
        document_embeddings.shape,
    )

    print(
        "Query Shape:",
        query_embedding.shape,
    )


if __name__ == "__main__":
    main()