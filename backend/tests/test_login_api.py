import pytest
from login_test_data import login_test_data
from api_client import login

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
    response = login(username, password)

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

