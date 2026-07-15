from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def main() -> None:
    print("Starting Authentication API Test")

    username = f"user-{uuid4()}"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "SecurePassword123!",
        },
    )

    assert register_response.status_code == 201

    register_data = register_response.json()

    assert register_data["success"] is True
    assert (
        register_data["user"]["username"]
        == username
    )

    print("Register Endpoint: PASS")

    duplicate_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "SecurePassword123!",
        },
    )

    assert duplicate_response.status_code == 409

    print("Duplicate User Handling: PASS")

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "SecurePassword123!",
        },
    )

    assert login_response.status_code == 200

    login_data = login_response.json()

    assert login_data["success"] is True
    assert login_data["access_token"]
    assert login_data["token_type"] == "bearer"

    print("Login Endpoint: PASS")

    invalid_login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "WrongPassword123!",
        },
    )

    assert (
        invalid_login_response.status_code
        == 401
    )

    invalid_login_data = (
        invalid_login_response.json()
    )

    assert (
        invalid_login_data["success"]
        is False
    )

    print("Invalid Login Handling: PASS")

    print()
    print("Authentication API Test Passed")


if __name__ == "__main__":
    main()