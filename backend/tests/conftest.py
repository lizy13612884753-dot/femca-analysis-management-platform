import os
import requests
import pytest

from config import base_url

login_url = f"{base_url}/api/auth/login/"

login_data = {
    "username": os.getenv("FEMCA_USERNAME"),
    "password": os.getenv("FEMCA_PASSWORD")
}

@pytest.fixture(scope="session")
def access_token():
    login_response = requests.post(
        login_url,
        json=login_data
    )

    assert login_response.status_code == 200

    token = login_response.json()["tokens"]["access"]

    return token