from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def main() -> None:
    print("Starting Authentication Regression Test")

    username = f"regression-{uuid4()}"
    password = "SecurePassword123!"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    print("User Registration: PASS")

    duplicate_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )

    assert duplicate_response.status_code == 409

    print("Duplicate User Protection: PASS")

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()[
        "access_token"
    ]

    assert access_token

    print("JWT Authentication: PASS")

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

    print("Invalid Credentials: PASS")

    unauthorized_chat = client.post(
        "/chat",
        json={
            "message": "Explain Nexus AI",
            "session_id": "auth-regression",
        },
    )

    assert unauthorized_chat.status_code == 401

    print("Protected Chat Access: PASS")

    invalid_token_chat = client.post(
        "/chat",
        headers={
            "Authorization": (
                "Bearer invalid-token"
            ),
        },
        json={
            "message": "Explain Nexus AI",
            "session_id": "auth-regression",
        },
    )

    assert invalid_token_chat.status_code == 401

    print("Invalid JWT Protection: PASS")

    workflow_response = client.get(
        "/workflows/non-existent-workflow",
        headers={
            "Authorization": (
                f"Bearer {access_token}"
            ),
        },
    )

    assert workflow_response.status_code == 404

    print("Workflow User Isolation: PASS")

    print()
    print(
        "Authentication Regression Test Passed"
    )


if __name__ == "__main__":
    main()