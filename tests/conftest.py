import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }


@pytest.fixture
def auth_headers(client, test_user):
    client.post("/auth/register", json=test_user)

    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }