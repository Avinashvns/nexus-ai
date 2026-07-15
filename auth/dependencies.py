import jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from auth.jwt import decode_access_token
from database.models.user import User
from database.repositories.user_repository import (
    user_repository,
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


def get_current_user(
    credentials: (
        HTTPAuthorizationCredentials | None
    ) = Depends(bearer_scheme),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        subject = payload.get("sub")

        if subject is None:
            raise HTTPException(
                status_code=(
                    status.HTTP_401_UNAUTHORIZED
                ),
                detail="Invalid authentication token",
            )

        user_id = int(subject)

    except (
        jwt.InvalidTokenError,
        ValueError,
    ) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        ) from error

    user = user_repository.get_by_id(
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user not found",
        )

    return user