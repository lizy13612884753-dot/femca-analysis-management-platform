import uuid

import pytest

from api_client import get_equipment, create_equipment, delete_equipment

import allure

import logging

logger = logging.getLogger(__name__)

def test_equipment(access_token):
    equipment_response = get_equipment(access_token)

    assert equipment_response.status_code == 200

    equipment_data = equipment_response.json()

    assert isinstance(equipment_data["count"], int)
    assert isinstance(equipment_data["results"], list)
    assert equipment_data["count"] >= len(equipment_data["results"]), (
        "Total equipment count cannot be smaller than returned results"
    )

    assert len(equipment_data["results"]) > 0

    for equipment in equipment_data["results"]:
        # Step 7：先检查字段是否存在
        assert "id" in equipment
        assert "name" in equipment, (
            f"Equipment ID {equipment.get('id', 'UNKNOWN')}: missing name field"
        )
        assert len(equipment["name"].strip()) > 0, (
            f"Equipment ID {equipment['id']}: name cannot be blank"
        )
        assert "serial_number" in equipment

        # 再检查字段类型
        assert isinstance(equipment["id"], int)
        assert isinstance(equipment["name"], str), (
            f"Equipment ID {equipment['id']}: name must be a string"
        )
        assert isinstance(equipment["serial_number"], str)

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
    equipment_type_id,
    equipment_cleanup
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": "A" * name_length
    }

    response = create_equipment(access_token, equipment_data)

    # 创建成功时，先记录 ID，确保测试结束后自动清理
    if response.status_code == 201:
        equipment_cleanup.append(response.json()["id"])

    assert response.status_code == expected_status

    response_data = response.json()

    if response.status_code == 201:
        assert response_data["name"] == equipment_data["name"]
        assert response_data["serial_number"] == equipment_data["serial_number"]

    if response.status_code == 400:
        assert "name" in response_data


def test_create_equipment_missing_name(
    access_token,
    equipment_type_id,
    equipment_cleanup
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}"
    }

    response = create_equipment(access_token, equipment_data)

    # 如果 API 意外创建成功，先记录 ID，确保后续能清理
    if response.status_code == 201:
        equipment_cleanup.append(response.json()["id"])

    assert response.status_code == 400

    response_data = response.json()
    assert "name" in response_data


def test_create_equipment_null_name(
    access_token,
    equipment_type_id,
    equipment_cleanup
):
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": None
    }

    response = create_equipment(access_token, equipment_data)

    if response.status_code == 201:
        equipment_cleanup.append(response.json()["id"])

    assert response.status_code == 400

    response_data = response.json()
    assert "name" in response_data

        
def test_create_equipment_invalid_equipment_type(
    access_token,
    equipment_cleanup
):
    equipment_data = {
        "equipment_type": 999999,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": "123"
    }

    response = create_equipment(access_token, equipment_data)

    # 如果意外创建成功，记录 ID 以便自动清理
    if response.status_code == 201:
        equipment_cleanup.append(response.json()["id"])

    assert response.status_code == 400

    response_data = response.json()
    assert "equipment_type" in response_data


def test_create_duplicate_equipment(
    access_token,
    equipment_type_id,
    equipment_cleanup
):
    serial_number = f"TEST-{uuid.uuid4().hex[:8]}"

    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": serial_number,
        "name": "Duplicate Test"
    }

    # 第一次创建：预期成功
    response = create_equipment(
        access_token,
        equipment_data
    )

    # 先记录 ID，确保后续断言失败时也能 Cleanup
    if response.status_code == 201:
        equipment_id = response.json()["id"]
        equipment_cleanup.append(equipment_id)

    assert response.status_code == 201

    # 第二次创建：相同 equipment_type + serial_number
    with allure.step("Verify duplicate equipment is rejected"):
        duplicate_response = create_equipment(
            access_token,
            equipment_data
        )

        duplicate_data = duplicate_response.json()

        allure.attach(
            str(duplicate_data),
            name="Duplicate Response Body",
            attachment_type=allure.attachment_type.TEXT
        )

        assert duplicate_response.status_code == 400
        assert "non_field_errors" in duplicate_data

    logger.info("Duplicate equipment correctly rejected")


def test_get_equipment_with_session(authenticated_session):
    assert "Authorization" in authenticated_session.headers

    response = get_equipment(session=authenticated_session)

    assert response.status_code == 200


def test_equipment_cleanup_fixture(
    equipment_cleanup,
    access_token,
    equipment_type_id
):

    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"CLEANUP-{uuid.uuid4().hex[:8]}",
        "name": "Cleanup Fixture Test"
    }

    response = create_equipment(access_token, equipment_data)

    if response.status_code == 201:
        equipment_id = response.json()["id"]
        equipment_cleanup.append(equipment_id)

    assert response.status_code == 201
    assert len(equipment_cleanup) == 1


def test_equipment_pagination(access_token):
    import requests
    from config import base_url

    url = f"{base_url}/api/equipment/instances/"

    response = get_equipment(
        access_token,
        params={"page": 1, "page_size": 5}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] >= len(data["results"])
    assert len(data["results"]) <= 5

    print("\nRequest URL:", response.url)
    print("Total count:", data.get("count"))
    print("Results length:", len(data.get("results", [])))
    print("Next page:", data.get("next"))
    print("Previous page:", data.get("previous"))


def test_equipment_invalid_page(access_token):
    # Step 1: 获取设备总数
    first_response = get_equipment(access_token)
    assert first_response.status_code == 200

    count = first_response.json()["count"]

    # Step 2: 计算一个超出范围的页码
    page_size = 20
    invalid_page = count // page_size + 2

    # Step 3: 请求超出范围的页码
    response = get_equipment(
        access_token,
        params={
            "page": invalid_page,
            "page_size": page_size
        }
    )

    print("\nTotal count:", count)
    print("Invalid page:", invalid_page)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    # Step 4: 验证当前接口行为
    assert response.status_code == 200

    data = response.json()
    assert data["results"] == []
    assert data["next"] is None


def test_missing_token_response():
    import requests
    from config import base_url

    url = f"{base_url}/api/equipment/instances/"

    response = requests.get(url)


    assert response.status_code == 401

    data = response.json()

    assert "detail" in data
    assert data["detail"] == "身份认证信息未提供。"


def test_invalid_token_response():
    import requests
    from config import base_url

    url = f"{base_url}/api/equipment/instances/"

    headers = {
        "Authorization": "Bearer invalid_token_123"
    }

    response = requests.get(
        url,
        headers=headers
    )



    assert response.status_code == 401

    data = response.json()

    assert data["code"] == "token_not_valid"
    assert data["messages"][0]["message"] == "令牌无效或已过期"



def test_expired_token_response():
    from datetime import timedelta
    import requests
    from rest_framework_simplejwt.tokens import AccessToken
    from config import base_url

    # Arrange: 准备过期 Token
    token = AccessToken()
    token.set_exp(lifetime=timedelta(seconds=-60))

    headers = {
        "Authorization": f"Bearer {str(token)}"
    }

    # Act: 发送请求
    response = requests.get(
        f"{base_url}/api/equipment/instances/",
        headers=headers
    )

    # Assert: 验证结果
    assert response.status_code == 401

    data = response.json()
    assert data["code"] == "token_not_valid"