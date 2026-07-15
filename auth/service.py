from auth.jwt import create_access_token
from auth.security import (
    hash_password,
    verify_password,
)
from database.models.user import User
from database.repositories.user_repository import (
    user_repository,
)


class AuthenticationService:
    def register_user(
        self,
        username: str,
        password: str,
    ) -> User:
        existing_user = (
            user_repository.get_by_username(
                username
            )
        )

        if existing_user is not None:
            raise ValueError(
                "Username already exists"
            )

        hashed_password = hash_password(
            password
        )

        return user_repository.create(
            username=username,
            hashed_password=hashed_password,
        )

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> str | None:
        user = (
            user_repository.get_by_username(
                username
            )
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return create_access_token(
            subject=str(user.id)
        )


authentication_service = (
    AuthenticationService()
)