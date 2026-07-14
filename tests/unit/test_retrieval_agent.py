from agents.retrieval import retrieval_agent
from models import AgentRequest
from rag.pipeline import rag_pipeline


def main():
    rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    request = AgentRequest(
        task="What is Nexus AI?"
    )

    response = retrieval_agent.run(request)

    print(response.model_dump())


if __name__ == "__main__":
    main()