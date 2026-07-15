from datetime import datetime, timezone

from sqlalchemy import select

from database.base import SessionLocal
from database.init_db import init_database
from database.models import WorkflowRun


def main():
    init_database()

    database = SessionLocal()

    workflow_id = "workflow-model-test"

    try:
        existing = database.scalar(
            select(WorkflowRun).where(
                WorkflowRun.workflow_id
                == workflow_id
            )
        )

        if existing:
            database.delete(existing)
            database.commit()

        workflow = WorkflowRun(
            workflow_id=workflow_id,
            session_id="test-session",
            task="Explain Nexus AI",
            status="running",
        )

        database.add(workflow)
        database.commit()
        database.refresh(workflow)

        assert workflow.id is not None
        assert workflow.status == "running"

        workflow.status = "completed"

        workflow.completed_at = datetime.now(
            timezone.utc
        )

        database.commit()
        database.refresh(workflow)

        stored_workflow = database.scalar(
            select(WorkflowRun).where(
                WorkflowRun.workflow_id
                == workflow_id
            )
        )

        assert stored_workflow is not None

        assert (
            stored_workflow.status
            == "completed"
        )

        assert (
            stored_workflow.completed_at
            is not None
        )

        print(
            {
                "id": stored_workflow.id,
                "workflow_id": (
                    stored_workflow.workflow_id
                ),
                "session_id": (
                    stored_workflow.session_id
                ),
                "task": stored_workflow.task,
                "status": stored_workflow.status,
                "created_at": str(
                    stored_workflow.created_at
                ),
                "completed_at": str(
                    stored_workflow.completed_at
                ),
            }
        )

    finally:
        database.close()

    print(
        "\nWorkflow Run Model Test Passed"
    )


if __name__ == "__main__":
    main()