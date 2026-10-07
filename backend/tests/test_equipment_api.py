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

        # ① 如果真的创建成功，先保存 ID，保证之后可以 cleanup
        if response.status_code == 201:
            equipment_id = response.json()["id"]

        # ② 再检查最核心的 Status Code
        assert response.status_code == expected_status

        # ③ Status 正确后，再做对应的 Response Body Validation
        response_data = response.json()

        if response.status_code == 201:
            assert response_data["name"] == equipment_data["name"]
            assert response_data["serial_number"] == equipment_data["serial_number"]

        if response.status_code == 400:
            assert "name" in response_data

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204

def test_create_equipment_missing_name(
    access_token,
    equipment_type_id
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}"
    }

    equipment_id = None

    try:
        response = create_equipment(access_token, equipment_data)

        if response.status_code == 201:
            equipment_id = response.json()["id"]

        assert response.status_code == 400

        response_data = response.json()
        assert "name" in response_data

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204


def test_create_equipment_null_name(
    access_token,
    equipment_type_id
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": None
    }

    equipment_id = None

    try:
        response = create_equipment(access_token, equipment_data)

        if response.status_code == 201:
            equipment_id = response.json()["id"]

        assert response.status_code == 400

        response_data = response.json()
        assert "name" in response_data

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204

        
def test_create_equipment_invalid_equipment_type(
    access_token
):
    equipment_data = {
        "equipment_type": 999999,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": "123"
    }

    equipment_id = None

    try:
        response = create_equipment(access_token, equipment_data)

        if response.status_code == 201:
            equipment_id = response.json()["id"]

        assert response.status_code == 400

        response_data = response.json()
        assert "equipment_type" in response_data

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204


def test_create_duplicate_equipment(
    access_token,
    equipment_type_id
):
    serial_number = f"TEST-{uuid.uuid4().hex[:8]}"

    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": serial_number,
        "name": "Duplicate Test"
    }

    equipment_id = None

    try:
        response = create_equipment(
            access_token,
            equipment_data
        )

        if response.status_code == 201:
            equipment_id = response.json()["id"]

        assert response.status_code == 201

        duplicate_response = create_equipment(
            access_token,
            equipment_data
        )

        duplicate_data = duplicate_response.json()

        assert duplicate_response.status_code == 400
        assert "non_field_errors" in duplicate_data

    finally:
        if equipment_id is not None:
            delete_response = delete_equipment(
                access_token,
                equipment_id
            )
            assert delete_response.status_code == 204
