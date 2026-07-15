from uuid import uuid4

from auth.jwt import decode_access_token
from auth.service import (
    authentication_service,
)
from database.init_db import init_database


def main() -> None:
    print("Starting Authentication Test")

    init_database()

    username = f"user-{uuid4()}"

    user = (
        authentication_service.register_user(
            username=username,
            password="SecurePassword123!",
        )
    )

    assert user.id is not None
    assert user.username == username

    print("User Registration: PASS")

    token = (
        authentication_service.authenticate_user(
            username=username,
            password="SecurePassword123!",
        )
    )

    assert token is not None

    print("User Authentication: PASS")

    payload = decode_access_token(token)

    assert payload["sub"] == str(user.id)

    print("JWT Access Token: PASS")

    invalid_token = (
        authentication_service.authenticate_user(
            username=username,
            password="WrongPassword",
        )
    )

    assert invalid_token is None

    print("Invalid Credentials: PASS")

    print()
    print("Authentication Test Passed")


if __name__ == "__main__":
    main()