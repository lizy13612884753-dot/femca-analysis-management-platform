import os
import requests

base_url = "http://127.0.0.1:8000"

login_url = f"{base_url}/api/auth/login/"

login_data = {
    "username": os.getenv("FEMCA_USERNAME"),
    "password": os.getenv("FEMCA_PASSWORD")
}

login_response = requests.post(
    login_url,
    json=login_data
)

print(login_response.status_code)

assert login_response.status_code == 200

access_token = login_response.json()["tokens"]["access"]

headers = {
    "Authorization": f"Bearer {access_token}"
}

equipment_url = f"{base_url}/api/equipment/instances/"

equipment_response = requests.get(
    equipment_url,
    headers=headers
)

equipment_data = equipment_response.json()

# 1. Status Code
assert equipment_response.status_code == 200

# 2. count exists
assert "count" in equipment_data

# 3. count Data Type
assert isinstance(equipment_data["count"], int)

# 4. results exists
assert "results" in equipment_data

# 5. Check every equipment
for equipment in equipment_data["results"]:
    assert "id" in equipment
    assert isinstance(equipment["id"], int)
    assert "name" in equipment
    assert "status" in equipment

print("Equipment API test passed!")