import requests
import pytest

def send_request(method, url, **kwargs):
    response = requests.request(
        method=method,
        url=url,
        **kwargs
    )

    return response

def login(username, password):
    login_url = "http://127.0.0.1:8000/api/auth/login/"

    login_data = {
        "username": username,
        "password": password
    }

    response = send_request(
        method="POST",
        url=login_url,
        json=login_data
    )

    return response

def test_login_success():

    response = login("admin", "admin123")

    result = response.json()

    assert response.status_code == 200
    assert result["user"]["username"] == "admin"
    assert "tokens" in result


@pytest.mark.parametrize(
    "username,password,error_field,expected_message",
    [
        ("admin", "wrong123", "non_field_errors", "用户名或密码错误"),
        ("", "admin123", "username", "该字段不能为空。"),
        ("admin", "", "password", "该字段不能为空。")
    ]
)
def test_login_fail(username, password, error_field, expected_message):

    response = login(username, password)

    result = response.json()

    assert response.status_code == 400
    assert result[error_field][0] == expected_message
    assert "tokens" not in result

def test_login_empty_username_and_password():

    response = login("", "")

    result = response.json()

    assert response.status_code == 400
    assert result["username"][0] == "该字段不能为空。"
    assert result["password"][0] == "该字段不能为空。"
    assert "tokens" not in result