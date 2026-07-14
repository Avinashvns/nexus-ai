from rag.pipeline import rag_pipeline
from workflow.engine import workflow_engine


def main():
    print("Starting Autonomous Workflow Test")

    rag_pipeline.ingest_pdf(
        "tests/data/sample.pdf"
    )

    response = workflow_engine.run(
        "Using the provided document, explain what Nexus AI does."
    )

    assert response.success is True
    assert response.output

    history = response.metadata[
        "execution_history"
    ]

    assert len(history) > 0

    for step in history:
        assert step["success"] is True
        assert step["attempts"] >= 1

    print("\nFinal Response:")
    print(response.output)

    print("\nExecution History:")

    for step in history:
        print(step)

    print("\nAutonomous Workflow Test Passed")


if __name__ == "__main__":
    main()