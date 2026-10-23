import uuid
from tests.api_client import create_equipment
from playwright.sync_api import expect
from tests.pages.equipment_page import EquipmentPage

def test_create_equipment_and_search_ui(
    access_token,
    equipment_type_id,
    equipment_cleanup,
    logged_in_page
):
    # TODO 1: 创建一个带随机标识的设备名称
    name = f"TEST-{uuid.uuid4().hex[:8]}"
    # TODO 2: 构造 equipment_data
    equipment_data = {
        "equipment_type": equipment_type_id,
        "serial_number": f"TEST-{uuid.uuid4().hex[:8]}",
        "name": name
    }
    # TODO 3: 调用 create_equipment()
    response = create_equipment(access_token, equipment_data)
    # TODO 4: 验证 status_code == 201
    assert response.status_code == 201
    # TODO 5: 把新设备 ID 加入 equipment_cleanup
    equipment_cleanup.append(response.json()["id"])
    # TODO 6: 创建 EquipmentPage 对象
    equipment_page = EquipmentPage(logged_in_page)
    # TODO 7: 打开设备实例页面
    equipment_page.open()
    # TODO 8: 搜索刚才创建的设备名称
    equipment_page.search(name)
    # TODO 9: 获取表格行 Locator
    equipment_rows = equipment_page.get_equipment_rows()
    # TODO 10: 验证只有一行，且包含正确的设备名称
    expect(equipment_rows).to_have_count(1)
    expect(equipment_rows.first).to_contain_text(name)