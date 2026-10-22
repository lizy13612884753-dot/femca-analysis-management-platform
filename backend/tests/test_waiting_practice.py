from playwright.sync_api import expect, Page
from tests.pages.equipment_page import EquipmentPage

def test_equipment_page_auto_waiting(logged_in_page: Page):
    equipment_page_auto_waiting = EquipmentPage(logged_in_page)
    equipment_page_auto_waiting.open()

    expect(logged_in_page).to_have_url(
        "http://localhost:8000/equipment/instances",
        timeout=10000
    )

def test_equipment_rows_locator(logged_in_page: Page):
    equipment_rows_locator = EquipmentPage(logged_in_page)
    equipment_rows_locator.open()
    equipment_rows_locator.search("导向轮")
    rows = equipment_rows_locator.get_equipment_rows()
    expect(rows).to_have_count(1)
    expect(rows.first).to_contain_text("导向轮")