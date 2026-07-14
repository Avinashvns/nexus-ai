from rag.pipeline import rag_pipeline
from workflow.engine import workflow_engine


def main():
    rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    response = workflow_engine.run(
        "Explain what Nexus AI does."
    )

    print("\nFinal Response:")
    print(response.output)

    print("\nMetadata:")
    print(response.metadata)


if __name__ == "__main__":
    main()