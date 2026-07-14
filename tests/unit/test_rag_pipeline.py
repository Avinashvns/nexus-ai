from rag.pipeline import rag_pipeline


def main():
    chunk_count = rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    print(
        f"Total Chunks Ingested: {chunk_count}"
    )

    results = rag_pipeline.retrieve(
        query="What is Nexus AI?",
        top_k=2,
    )

    print("\nRetrieved Context:")

    for result in results:
        print(result)


if __name__ == "__main__":
    main()