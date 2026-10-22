from playwright.sync_api import Page, expect
from tests.pages.equipment_page import EquipmentPage

def test_equipment_page_navigation(logged_in_page: Page):
    page = logged_in_page

    equipment_page = EquipmentPage(page)
    equipment_page.open()

    expect(page).to_have_url(
        "http://localhost:8000/equipment/instances",
        timeout=10000
    )

def test_equipment_page_search(logged_in_page: Page):
    # TODO 1: 將 logged_in_page 保存到 page
	page = logged_in_page
    # TODO 2: 建立 EquipmentPage Object
	equipment_page_search = EquipmentPage(page)
    # TODO 3: 呼叫 open() 進入設備頁面
	equipment_page_search.open()
    # TODO 4: 呼叫 search() 搜尋「导向轮」
	equipment_page_search.search("导向轮")
    # TODO 5: 找到設備表格的 Rows
	equipment_rows = page.locator(".el-table__body tbody tr")
    # TODO 6: 驗證只有 1 Row
	expect(equipment_rows).to_have_count(1)
    # TODO 7: 驗證該 Row 包含「导向轮」
	expect(equipment_rows.first).to_contain_text("导向轮")