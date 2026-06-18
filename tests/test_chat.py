def test_chat_invalid_report(
    client,
    auth_headers
):
    response = client.post(
        "/chat/99999/ask",
        headers=auth_headers,
        json={
            "question": "What is wrong?",
            "language": "English"
        }
    )

    assert response.status_code == 404