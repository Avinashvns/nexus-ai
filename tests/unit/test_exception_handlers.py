from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from api.exception_handlers import (
    register_exception_handlers,
)


def main():
    app = FastAPI()

    register_exception_handlers(app)

    @app.get("/http-error")
    def http_error():
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    @app.get("/server-error")
    def server_error():
        raise RuntimeError(
            "Sensitive internal error"
        )

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    http_response = client.get(
        "/http-error"
    )

    assert http_response.status_code == 404

    http_data = http_response.json()

    assert http_data["success"] is False

    assert (
        http_data["error"]["type"]
        == "HTTPException"
    )

    assert (
        http_data["error"]["message"]
        == "Resource not found"
    )

    server_response = client.get(
        "/server-error"
    )

    assert server_response.status_code == 500

    server_data = server_response.json()

    assert server_data["success"] is False

    assert (
        server_data["error"]["type"]
        == "InternalServerError"
    )

    assert (
        server_data["error"]["message"]
        == "Internal server error"
    )

    assert (
        "Sensitive internal error"
        not in server_response.text
    )

    print("HTTP Exception Response:")
    print(http_data)

    print("\nGlobal Exception Response:")
    print(server_data)

    print(
        "\nException Handler Test Passed"
    )


if __name__ == "__main__":
    main()