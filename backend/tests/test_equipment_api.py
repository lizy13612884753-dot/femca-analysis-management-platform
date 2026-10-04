import pytest
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