def test_get_reports_requires_auth(client):
    response = client.get("/reports/list")

    assert response.status_code == 401


def test_upload_non_pdf_file(client, auth_headers):
    response = client.post(
        "/reports/upload",
        headers=auth_headers,
        files={
            "file": (
                "test.txt",
                b"not a pdf",
                "text/plain"
            )
        }
    )

    assert response.status_code in [400, 422]