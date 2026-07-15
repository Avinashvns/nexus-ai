from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select

from database.base import SessionLocal
from database.models import WorkflowRun


class WorkflowRepository:
    def create(
        self,
        workflow_id: str,
        session_id: str,
        task: str,
    ) -> WorkflowRun:
        database = SessionLocal()

        try:
            workflow = WorkflowRun(
                workflow_id=workflow_id,
                session_id=session_id,
                task=task,
                status="running",
            )

            database.add(workflow)
            database.commit()
            database.refresh(workflow)

            database.expunge(workflow)

            return workflow

        except Exception:
            database.rollback()
            raise

        finally:
            database.close()

    def get(
        self,
        workflow_id: str,
    ) -> WorkflowRun | None:
        database = SessionLocal()

        try:
            workflow = database.scalar(
                select(WorkflowRun).where(
                    WorkflowRun.workflow_id
                    == workflow_id
                )
            )

            if workflow is not None:
                database.expunge(workflow)

            return workflow

        finally:
            database.close()

    def mark_completed(
        self,
        workflow_id: str,
        metrics: dict[str, Any],
        execution_history: list[
            dict[str, Any]
        ],
    ) -> None:
        database = SessionLocal()

        try:
            workflow = self._get_workflow(
                database=database,
                workflow_id=workflow_id,
            )

            workflow.status = "completed"
            workflow.metrics = metrics
            workflow.execution_history = (
                execution_history
            )
            workflow.completed_at = datetime.now(
                timezone.utc
            )

            database.commit()

        except Exception:
            database.rollback()
            raise

        finally:
            database.close()

    def mark_failed(
        self,
        workflow_id: str,
        metrics: dict[str, Any],
        execution_history: list[
            dict[str, Any]
        ],
    ) -> None:
        database = SessionLocal()

        try:
            workflow = self._get_workflow(
                database=database,
                workflow_id=workflow_id,
            )

            workflow.status = "failed"
            workflow.metrics = metrics
            workflow.execution_history = (
                execution_history
            )
            workflow.completed_at = datetime.now(
                timezone.utc
            )

            database.commit()

        except Exception:
            database.rollback()
            raise

        finally:
            database.close()

    @staticmethod
    def _get_workflow(
        database,
        workflow_id: str,
    ) -> WorkflowRun:
        workflow = database.scalar(
            select(WorkflowRun).where(
                WorkflowRun.workflow_id
                == workflow_id
            )
        )

        if workflow is None:
            raise ValueError(
                f"Workflow not found: {workflow_id}"
            )

        return workflow


workflow_repository = WorkflowRepository()