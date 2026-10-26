import os
from tests.api_client import login

def test_ci_login_success():
    username = os.getenv("FEMCA_USERNAME")
    password = os.getenv("FEMCA_PASSWORD")

    assert username and password, "Missing FEMCA test credentials"

    response = login(username, password)
    assert response.status_code == 200
    assert "access" in response.json()["tokens"]
