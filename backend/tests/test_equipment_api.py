import uuid

import pytest

from api_client import get_equipment, create_equipment, delete_equipment


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

@pytest.mark.parametrize(
    "token, expected_status, expected_key, expected_value",
    [
        pytest.param(
            None,
            401,
            "detail",
            "身份认证信息未提供。",
            id="missing-token"
        ),
        pytest.param(
            "definitely_invalid_token",
            401,
            "code",
            "token_not_valid",
            id="invalid-token"
        )
    ]
)
def test_equipment_auth(
    token,
    expected_status,
    expected_key,
    expected_value
):
    equipment_response = get_equipment(token)
    equipment_data = equipment_response.json()

    assert equipment_response.status_code == expected_status
    assert equipment_data[expected_key] == expected_value


@pytest.mark.parametrize(
    "name_length, expected_status",
    [
        pytest.param(199, 201, id="name-199"),
        pytest.param(200, 201, id="name-200"),
        pytest.param(201, 400, id="name-201"),
    ]
)
def test_equipment_name_boundary(
    name_length,
    expected_status,
    access_token,
    equipment_type_id
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": "A" * name_length
    }

    equipment_id = None

    try:
        response = create_equipment(access_token, equipment_data)

        if response.status_code == 201:
            equipment_id = response.json()["id"]

        assert response.status_code == expected_status

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204
