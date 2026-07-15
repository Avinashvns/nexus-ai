from unittest.mock import patch

from database.init_db import init_database
from database.repositories import workflow_repository
from models import AgentResponse
from workflow.engine import workflow_engine


def main():
    print(
        "Starting Workflow Execution Data Test"
    )

    init_database()

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
                session_id="execution-data-test",
            )

    assert response.success is True

    workflow_id = response.metadata[
        "workflow_id"
    ]

    workflow = workflow_repository.get(
        workflow_id
    )

    assert workflow is not None

    assert workflow.status == "completed"

    assert workflow.metrics is not None

    assert (
        workflow.metrics["workflow_success"]
        is True
    )

    assert (
        workflow.metrics["agent_count"]
        == 1
    )

    assert (
        workflow.execution_history
        is not None
    )

    assert (
        workflow.execution_history[0]["agent"]
        == "ReasoningAgent"
    )

    print("\nMetrics:")
    print(workflow.metrics)

    print("\nExecution History:")
    print(workflow.execution_history)

    print(
        "\nWorkflow Execution Data Test Passed"
    )


if __name__ == "__main__":
    main()