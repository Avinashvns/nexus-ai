from unittest.mock import patch

from models import AgentResponse
from workflow.engine import workflow_engine


def main():
    print("Starting Workflow Metrics Test")

    planner_response = AgentResponse(
        success=True,
        output=[
            {
                "id": 1,
                "task": "Analyze Nexus AI",
                "agent": "ReasoningAgent",
                "priority": 1,
                "status": "pending",
            }
        ],
        metadata={
            "agent": "PlannerAgent",
        },
    )

    agent_response = AgentResponse(
        success=True,
        output="Nexus AI analysis",
        metadata={
            "agent": "ReasoningAgent",
        },
    )

    with patch(
        "workflow.engine.planner_agent.run",
        return_value=planner_response,
    ):
        with patch(
            "workflow.engine.agent_executor.execute",
            return_value=agent_response,
        ):
            response = workflow_engine.run(
                task="Analyze Nexus AI",
                session_id="metrics-test",
            )

    assert response.success is True

    metrics = response.metadata["metrics"]

    assert metrics["workflow_success"] is True
    assert metrics["workflow_duration_seconds"] >= 0
    assert metrics["agent_count"] == 1

    assert (
        metrics["agents"][0]["agent"]
        == "ReasoningAgent"
    )

    assert (
        metrics["agents"][0]["success"]
        is True
    )

    print("\nWorkflow Metrics:")
    print(metrics)

    print(
        "\nWorkflow Metrics Test Passed"
    )


if __name__ == "__main__":
    main()