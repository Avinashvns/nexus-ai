from agents.retrieval import retrieval_agent
from models import AgentRequest
from rag.pipeline import rag_pipeline


def main():
    print("Starting RAG Integration Test")

    chunk_count = rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    assert chunk_count > 0

    request = AgentRequest(
        task="What does the RAG engine do?"
    )

    response = retrieval_agent.run(request)

    assert response.success is True
    assert len(response.output) > 0

    top_result = response.output[0]

    assert "content" in top_result
    assert "score" in top_result

    print("\nTop Retrieved Context:")
    print(top_result)

    print("\nRAG Integration Test Passed")


if __name__ == "__main__":
    main()