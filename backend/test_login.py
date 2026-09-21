import requests

login_url = "http://127.0.0.1:8000/api/auth/login/"

login_data = {
    "username": "admin",
    "password": "admin123"
}

response = requests.post(
    url=login_url,
    json=login_data
)

result = response.json()

username = result["user"]["username"]
access_token = result["tokens"]["access"]
refresh_token = result["tokens"]["refresh"]

assert response.status_code == 200
assert username == "admin"
assert access_token != ""
assert refresh_token != ""

print("登录接口测试 PASS")