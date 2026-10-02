import os
import requests
import pytest


base_url = "http://127.0.0.1:8000"

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

def test_equipment(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    equipment_url = f"{base_url}/api/equipment/instances/"

    equipment_response = requests.get(
        equipment_url,
        headers=headers
    )

    equipment_data = equipment_response.json()

    assert equipment_response.status_code == 200
    assert "count" in equipment_data
    assert isinstance(equipment_data["count"], int)
    assert "results" in equipment_data

    for equipment in equipment_data["results"]:
        assert "id" in equipment
        assert isinstance(equipment["id"], int)
        assert "name" in equipment
        assert "status" in equipment