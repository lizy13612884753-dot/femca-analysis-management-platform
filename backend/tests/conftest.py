import os
import pytest
from api_client import login, get_equipment_types


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

@pytest.fixture(scope="session")
def equipment_type_id(access_token):
    response = get_equipment_types(access_token)
    data = response.json()

    assert response.status_code == 200
    assert len(data["results"]) > 0

    equipment_type_id = data["results"][0]["id"]

    return equipment_type_id
    