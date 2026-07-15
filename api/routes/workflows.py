from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from auth.dependencies import get_current_user
from database.models.user import User
from database.repositories import (
    workflow_repository,
)


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"],
)


@router.get("/{workflow_id}")
def get_workflow(
    workflow_id: str,
    current_user: User = Depends(
        get_current_user
    ),
) -> dict:
    workflow = workflow_repository.get(
        workflow_id=workflow_id,
        user_id=current_user.id,
    )

    if workflow is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return {
        "success": True,
        "workflow": {
            "workflow_id": workflow.workflow_id,
            "session_id": workflow.session_id,
            "task": workflow.task,
            "status": workflow.status,
            "metrics": workflow.metrics,
            "execution_history": (
                workflow.execution_history
            ),
            "created_at": (
                workflow.created_at.isoformat()
            ),
            "completed_at": (
                workflow.completed_at.isoformat()
                if workflow.completed_at
                else None
            ),
        },
    }