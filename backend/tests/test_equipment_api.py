from api_client import get_equipment


def test_equipment(access_token):
    equipment_response = get_equipment(access_token)

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