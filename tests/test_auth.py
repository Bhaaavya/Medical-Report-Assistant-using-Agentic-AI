def test_register_user(client, test_user):
    response = client.post("/auth/register", json=test_user)

    assert response.status_code in [200, 400]


def test_login_user(client, test_user):
    client.post("/auth/register", json=test_user)

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert "email" in response.json()