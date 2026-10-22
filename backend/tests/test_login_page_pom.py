from playwright.sync_api import Page, expect
from tests.pages.login_page import LoginPage
import os

def test_login_page_open(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    expect(page).to_have_url("http://localhost:8000/login")

def test_login_page_valid_credentials(page: Page):
    username = os.getenv("FEMCA_TEST_USERNAME")
    password = os.getenv("FEMCA_TEST_PASSWORD")

    assert username and password, "Missing FEMCA test credentials"

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(username, password)

    expect(page).to_have_url(
        "http://localhost:8000/dashboard",
        timeout=10000
    )

def test_login_page_invalid_credentials(page: Page):
    login_page_invalid = LoginPage(page)

    login_page_invalid.open()
    login_page_invalid.login("wrong_user", "wrong_password")

    expect(page.get_by_role("alert")).to_contain_text("登录失败")
    expect(page).to_have_url("http://localhost:8000/login")