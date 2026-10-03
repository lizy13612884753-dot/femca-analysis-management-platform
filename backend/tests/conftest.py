import os
import pytest
from api_client import login


login_data = {
    "username": os.getenv("FEMCA_USERNAME"),
    "password": os.getenv("FEMCA_PASSWORD")
}

@pytest.fixture(scope="session")
def access_token():
    login_response = login(
        login_data["username"],
        login_data["password"]
    )

    assert login_response.status_code == 200

    token = login_response.json()["tokens"]["access"]

    return token