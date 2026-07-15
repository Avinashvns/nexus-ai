from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def main() -> None:
    print("Starting Protected Chat API Test")

    unauthorized_response = client.post(
        "/chat",
        json={
            "task": "Explain Nexus AI",
            "session_id": "protected-test",
        },
    )

    assert (
        unauthorized_response.status_code
        == 401
    )

    print("Unauthorized Chat Access: PASS")

    username = f"user-{uuid4()}"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "SecurePassword123!",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "SecurePassword123!",
        },
    )

    assert login_response.status_code == 200

    access_token = (
        login_response.json()["access_token"]
    )

    print("JWT Authentication: PASS")

    invalid_token_response = client.post(
        "/chat",
        headers={
            "Authorization": (
                "Bearer invalid-token"
            ),
        },
        json={
            "task": "Explain Nexus AI",
            "session_id": "protected-test",
        },
    )

    assert (
        invalid_token_response.status_code
        == 401
    )

    print("Invalid JWT Rejection: PASS")

    print()
    print("Protected Chat API Test Passed")


if __name__ == "__main__":
    main()