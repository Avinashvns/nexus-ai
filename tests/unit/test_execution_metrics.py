from time import sleep

from observability.metrics import ExecutionMetrics


def main():
    metrics = ExecutionMetrics()

    metrics.start_workflow()

    metrics.start_agent(
        "ReasoningAgent"
    )

    sleep(0.1)

    metrics.end_agent(
        agent_name="ReasoningAgent",
        success=True,
    )

    result = metrics.finish_workflow(
        success=True
    )

    assert result["workflow_success"] is True

    assert result["workflow_duration_seconds"] > 0

    assert result["agent_count"] == 1

    assert (
        result["agents"][0]["agent"]
        == "ReasoningAgent"
    )

    assert (
        result["agents"][0][
            "duration_seconds"
        ]
        > 0
    )

    print(result)

    print(
        "\nExecution Metrics Test Passed"
    )


if __name__ == "__main__":
    main()