from playwright.sync_api import Page

class EquipmentPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.get_by_role("menuitem", name="设备管理").click()
        self.page.get_by_role("menuitem", name="设备实例").click()

    def search(self, keyword):
        search_input = self.page.get_by_placeholder("搜索设备实例...")
        search_input.fill(keyword)
        search_input.press("Enter")

    def get_equipment_rows(self):
        equipment_rows = self.page.locator(".el-table__body tbody tr")
        return equipment_rows
