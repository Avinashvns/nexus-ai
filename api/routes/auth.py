from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from api.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)
from auth.service import (
    authentication_service,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegisterRequest,
) -> dict:
    try:
        user = (
            authentication_service.register_user(
                username=request.username,
                password=request.password,
            )
        )

        return {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post("/login")
def login_user(
    request: LoginRequest,
) -> dict:
    token = (
        authentication_service.authenticate_user(
            username=request.username,
            password=request.password,
        )
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer",
    }