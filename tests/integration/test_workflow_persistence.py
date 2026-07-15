from unittest.mock import patch

from database.init_db import init_database
from database.repositories import workflow_repository
from models import AgentResponse
from workflow.engine import workflow_engine


def main():
    print(
        "Starting Workflow Persistence Test"
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
                session_id="workflow-persistence-test",
            )

    assert response.success is True

    workflow_id = response.metadata[
        "workflow_id"
    ]

    stored_workflow = workflow_repository.get(
        workflow_id
    )

    assert stored_workflow is not None

    assert (
        stored_workflow.workflow_id
        == workflow_id
    )

    assert (
        stored_workflow.session_id
        == "workflow-persistence-test"
    )

    assert (
        stored_workflow.task
        == "Analyze Nexus AI"
    )

    assert (
        stored_workflow.status
        == "completed"
    )

    assert (
        stored_workflow.completed_at
        is not None
    )

    print("\nPersisted Workflow:")

    print(
        {
            "workflow_id": (
                stored_workflow.workflow_id
            ),
            "session_id": (
                stored_workflow.session_id
            ),
            "task": stored_workflow.task,
            "status": stored_workflow.status,
            "completed_at": str(
                stored_workflow.completed_at
            ),
        }
    )

    print(
        "\nWorkflow Persistence Test Passed"
    )


if __name__ == "__main__":
    main()