import requests

login_url = "http://127.0.0.1:8000/api/auth/login/"

login_data = {
    "username": "admin",
    "password": "wrong123"
}

response = requests.post(
    url=login_url,
    json=login_data
)

result = response.json()

error_message = result["non_field_errors"][0]

assert response.status_code == 400
assert error_message == "用户名或密码错误"
assert "tokens" not in result

print("错误密码登录测试 PASS")