from fastapi.testclient import TestClient

from main import app


client = TestClient(
    app,
    raise_server_exceptions=False,
)


def main():
    print(
        "Starting Production Hardening Test"
    )

    health_response = client.get("/health")

    assert health_response.status_code == 200

    assert (
        health_response.headers[
            "x-content-type-options"
        ]
        == "nosniff"
    )

    assert (
        health_response.headers[
            "x-frame-options"
        ]
        == "DENY"
    )

    assert (
        health_response.headers[
            "referrer-policy"
        ]
        == "no-referrer"
    )

    assert (
        health_response.headers[
            "cache-control"
        ]
        == "no-store"
    )

    invalid_chat_response = client.post(
        "/chat",
        json={
            "task": "   ",
            "session_id": "test-session",
        },
    )

    assert (
        invalid_chat_response.status_code
        == 422
    )

    invalid_chat_data = (
        invalid_chat_response.json()
    )

    assert (
        invalid_chat_data["success"]
        is False
    )

    assert (
        invalid_chat_data["error"]["type"]
        == "ValidationError"
    )

    invalid_upload_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                b"Not a PDF",
                "text/plain",
            )
        },
    )

    assert (
        invalid_upload_response.status_code
        == 415
    )

    invalid_upload_data = (
        invalid_upload_response.json()
    )

    assert (
        invalid_upload_data["success"]
        is False
    )

    missing_workflow_response = client.get(
        "/workflows/non-existent-workflow"
    )

    assert (
        missing_workflow_response.status_code
        == 404
    )

    missing_workflow_data = (
        missing_workflow_response.json()
    )

    assert (
        missing_workflow_data["success"]
        is False
    )

    print("\nSecurity Headers: PASS")
    print("Request Validation: PASS")
    print("Upload Safety: PASS")
    print("Global Error Format: PASS")
    print("HTTP Error Handling: PASS")

    print(
        "\nProduction Hardening Test Passed"
    )


if __name__ == "__main__":
    main()