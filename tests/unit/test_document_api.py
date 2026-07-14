from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def main():
    with open(
        "tests/data/sample.pdf",
        "rb",
    ) as file:
        response = client.post(
            "/documents/upload",
            files={
                "file": (
                    "sample.pdf",
                    file,
                    "application/pdf",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["chunk_count"] > 0

    print(data)

    print(
        "\nDocument API Test Passed"
    )


if __name__ == "__main__":
    main()