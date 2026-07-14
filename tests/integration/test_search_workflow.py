from workflow.engine import workflow_engine


def main():
    print("Starting Full Search Workflow Test")

    response = workflow_engine.run(
        task=(
            "Search the web and explain Agentic AI."
        ),
        session_id="search-workflow-test",
    )

    assert response.success is True
    assert response.output

    history = response.metadata[
        "execution_history"
    ]

    agents = [
        step["agent"]
        for step in history
    ]

    assert agents == [
        "SearchAgent",
        "ReasoningAgent",
        "CriticAgent",
        "WriterAgent",
    ]

    for step in history:
        assert step["success"] is True
        assert step["attempts"] >= 1

    print("\nFinal Response:")
    print(response.output)

    print("\nExecution History:")

    for step in history:
        print(step)

    print("\nFull Search Workflow Test Passed")


if __name__ == "__main__":
    main()