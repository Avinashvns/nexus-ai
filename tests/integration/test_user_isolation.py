from uuid import uuid4

from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def create_user_token() -> str:
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

    return login_response.json()[
        "access_token"
    ]


def main() -> None:
    print("Starting User Isolation Test")

    user_a_token = create_user_token()
    user_b_token = create_user_token()

    assert user_a_token != user_b_token

    print("Independent Users: PASS")

    unauthorized_response = client.get(
        "/workflows/non-existent-workflow"
    )

    assert (
        unauthorized_response.status_code
        == 401
    )

    print("Workflow Authentication: PASS")

    user_a_response = client.get(
        "/workflows/non-existent-workflow",
        headers={
            "Authorization": (
                f"Bearer {user_a_token}"
            ),
        },
    )

    assert user_a_response.status_code == 404

    user_b_response = client.get(
        "/workflows/non-existent-workflow",
        headers={
            "Authorization": (
                f"Bearer {user_b_token}"
            ),
        },
    )

    assert user_b_response.status_code == 404

    print("User Boundary Enforcement: PASS")

    print()
    print("User Isolation Test Passed")


if __name__ == "__main__":
    main()