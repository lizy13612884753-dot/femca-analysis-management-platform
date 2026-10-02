import requests

base_url = "http://127.0.0.1:8000"


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