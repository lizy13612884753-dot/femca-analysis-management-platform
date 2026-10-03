import requests
import pytest
from config import base_url
from login_test_data import login_test_data

login_url = f"{base_url}/api/auth/login/"


@pytest.mark.parametrize(
    "username,password,expected_status,expected_message",
    login_test_data
)
def test_login(
    username,
    password,
    expected_status,
    expected_message
):
    login_data = {
        "username": username,
        "password": password
    }

    response = requests.post(
        login_url,
        json=login_data
    )

    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()

        assert "user" in data
        assert "tokens" in data

        assert "access" in data["tokens"]
        assert "refresh" in data["tokens"]

        assert data["tokens"]["access"]
        assert data["tokens"]["refresh"]

    if expected_message is not None:
        data = response.json()
        assert data["non_field_errors"][0] == expected_message

