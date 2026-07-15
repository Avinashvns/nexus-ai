from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def main():
    invalid_type_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                b"Hello Nexus AI",
                "text/plain",
            )
        },
    )

    assert (
        invalid_type_response.status_code
        == 415
    )

    fake_pdf_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "fake.pdf",
                b"This is not a PDF",
                "application/pdf",
            )
        },
    )

    assert fake_pdf_response.status_code == 400

    empty_pdf_response = client.post(
        "/documents/upload",
        files={
            "file": (
                "empty.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert empty_pdf_response.status_code == 400

    print(
        "Upload Safety Test Passed"
    )


if __name__ == "__main__":
    main()