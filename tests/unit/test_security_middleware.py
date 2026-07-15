from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.middleware import (
    SecurityHeadersMiddleware,
)


def main():
    app = FastAPI()

    app.add_middleware(
        SecurityHeadersMiddleware
    )

    @app.get("/test")
    def test_route():
        return {
            "success": True,
        }

    client = TestClient(app)

    response = client.get("/test")

    assert response.status_code == 200

    assert (
        response.headers[
            "x-content-type-options"
        ]
        == "nosniff"
    )

    assert (
        response.headers["x-frame-options"]
        == "DENY"
    )

    assert (
        response.headers["referrer-policy"]
        == "no-referrer"
    )

    assert (
        response.headers["cache-control"]
        == "no-store"
    )

    print("Security Headers:")

    print(
        {
            "x-content-type-options": (
                response.headers[
                    "x-content-type-options"
                ]
            ),
            "x-frame-options": (
                response.headers[
                    "x-frame-options"
                ]
            ),
            "referrer-policy": (
                response.headers[
                    "referrer-policy"
                ]
            ),
            "cache-control": (
                response.headers[
                    "cache-control"
                ]
            ),
        }
    )

    print(
        "\nSecurity Middleware Test Passed"
    )


if __name__ == "__main__":
    main()