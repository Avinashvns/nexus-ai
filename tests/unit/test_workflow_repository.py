from uuid import uuid4

from database.init_db import init_database
from database.repositories import (
    workflow_repository,
)


def main():
    init_database()

    workflow_id = str(uuid4())

    created = workflow_repository.create(
        workflow_id=workflow_id,
        session_id="repository-test",
        task="Explain Nexus AI",
    )

    assert created.workflow_id == workflow_id
    assert created.status == "running"

    stored = workflow_repository.get(workflow_id)

    assert stored is not None
    assert stored.status == "running"

    workflow_repository.mark_completed(
        workflow_id=workflow_id,
        metrics={
            "workflow_success": True,
            "workflow_duration_seconds": 1.5,
            "agent_count": 1,
            "agents": [],
        },
        execution_history=[
            {
                "step_id": 1,
                "agent": "ReasoningAgent",
                "success": True,
                "attempts": 1,
            }
        ],
    )
    completed = workflow_repository.get(workflow_id)

    assert completed is not None
    assert completed.status == "completed"
    assert completed.completed_at is not None

    assert completed.metrics is not None

    assert completed.metrics["workflow_success"] is True

    assert completed.execution_history is not None

    assert completed.execution_history[0]["agent"] == "ReasoningAgent"

    print(
        {
            "workflow_id": completed.workflow_id,
            "session_id": completed.session_id,
            "task": completed.task,
            "status": completed.status,
            "completed_at": str(completed.completed_at),
        }
    )

    print("\nWorkflow Repository Test Passed")


if __name__ == "__main__":
    main()
