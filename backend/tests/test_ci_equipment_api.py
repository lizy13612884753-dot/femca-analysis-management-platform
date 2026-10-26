import os
from tests.api_client import login, get_equipment

def test_ci_get_equipment_list():
    username = os.getenv("FEMCA_USERNAME")
    password = os.getenv("FEMCA_PASSWORD")
    
    assert username and password, "Missing FEMCA test credentials"
    
    login_response = login(username, password)
    assert login_response.status_code == 200

    token = login_response.json()["tokens"]["access"]
    equipment_response = get_equipment(token)
    assert equipment_response.status_code == 200
    assert isinstance(equipment_response.json()["results"], list)
    results = equipment_response.json()["results"]
    assert any(
        item["serial_number"] == "CI-001"
        for item in results
    )