from rag.pipeline import rag_pipeline
from workflow.engine import workflow_engine


def main():
    session_id = "memory-test"

    rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    first_response = workflow_engine.run(
        task="Explain what Nexus AI does.",
        session_id=session_id,
    )

    assert first_response.success is True

    print("\nFirst Response:")
    print(first_response.output)

    second_response = workflow_engine.run(
        task="What did I ask you before?",
        session_id=session_id,
    )

    assert second_response.success is True

    print("\nSecond Response:")
    print(second_response.output)

    print("\nWorkflow Memory Test Passed")


if __name__ == "__main__":
    main()