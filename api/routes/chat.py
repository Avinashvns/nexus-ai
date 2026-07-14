from fastapi import APIRouter, HTTPException, status

from api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from core.logger import app_logger
from workflow.engine import workflow_engine


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
) -> ChatResponse:
    try:
        result = workflow_engine.run(
            task=request.message,
            session_id=request.session_id,
        )

        if not result.success:
            app_logger.error(
                "Chat workflow execution failed"
            )

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
        app_logger.exception(
            f"Chat API Error: {error}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from error