from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("http://localhost:8000/login")

    def login(self, username, password):
        self.page.get_by_role("textbox", name="用户名").fill(username)
        self.page.get_by_placeholder("密码").fill(password)
        self.page.get_by_role("button", name="登录").click()
