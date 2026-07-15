from fastapi import APIRouter, HTTPException, status

from api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from core.logger import app_logger
from workflow.engine import workflow_engine

from fastapi import Depends

from auth.dependencies import get_current_user
from database.models.user import User


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)

def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    try:
        result = workflow_engine.run(
            task=request.message,
            session_id=request.session_id,
            user_id=current_user.id,
        )

        if not result.success:
            app_logger.error("Chat workflow execution failed")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "Workflow execution failed",
                    "metadata": result.metadata,
                },
            )

        return ChatResponse(
            success=True,
            response=result.output,
            metadata=result.metadata,
        )

    except HTTPException:
        raise

    except Exception as error:
        app_logger.exception(f"Chat API Error: {error}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from error
