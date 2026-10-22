import os
from playwright.sync_api import Page, expect
import pytest



def test_femca_login_page(page: Page):
    page.goto("http://localhost:8000/login")

    expect(page.get_by_role("textbox", name="用户名")).to_be_visible()
    expect(page.get_by_placeholder("密码")).to_be_visible()
    expect(page.get_by_role("button", name="登录")).to_be_visible()

def test_femca_login_invalid_credentials(page: Page):
    page.goto("http://localhost:8000/login")

    page.get_by_role("textbox", name="用户名").fill("invalid_user_123")
    page.get_by_placeholder("密码").fill("wrong_password_123")
    page.get_by_role("button", name="登录").click()

    expect(page.get_by_role("alert")).to_contain_text("登录失败")
    expect(page).to_have_url("http://localhost:8000/login")

def test_femca_login_valid_credentials(page: Page):
    username = os.getenv("FEMCA_TEST_USERNAME")
    password = os.getenv("FEMCA_TEST_PASSWORD")

    assert username and password, "Missing FEMCA test credentials"

    page.goto("http://localhost:8000/login")

    page.get_by_role("textbox", name="用户名").fill(username)
    page.get_by_placeholder("密码").fill(password)
    page.get_by_role("button", name="登录").click()


    expect(page).to_have_url(
        "http://localhost:8000/dashboard",
        timeout=10000
    )

    expect(page.get_by_text("设备管理")).to_be_visible()

def test_femca_equipment_navigation(page: Page):
    username = os.getenv("FEMCA_TEST_USERNAME")
    password = os.getenv("FEMCA_TEST_PASSWORD")

    assert username and password, "Missing FEMCA test credentials"

    page.goto("http://localhost:8000/login")

    page.get_by_role("textbox", name="用户名").fill(username)
    page.get_by_placeholder("密码").fill(password)
    page.get_by_role("button", name="登录").click()

    expect(page).to_have_url(
        "http://localhost:8000/dashboard",
        timeout=10000
    )

    page.get_by_role("menuitem", name="设备管理").click()
    page.get_by_role("menuitem", name="设备实例").click()

    expect(page).to_have_url(
        "http://localhost:8000/equipment/instances",
        timeout=10000
    )

    expect(page.get_by_text("设备实例管理")).to_be_visible()

def test_femca_equipment_search(logged_in_page: Page):
    page = logged_in_page

    page.get_by_role("menuitem", name="设备管理").click()
    page.get_by_role("menuitem", name="设备实例").click()

    expect(page).to_have_url(
        "http://localhost:8000/equipment/instances",
        timeout=10000
    )

    search_input = page.get_by_placeholder("搜索设备实例...")

    search_input.fill("导向轮")
    search_input.press("Enter")

    expect(page.get_by_text("导向轮")).to_be_visible()
    equipment_rows = page.locator(".el-table__body tbody tr")
    expect(equipment_rows).to_have_count(1)
    expect(equipment_rows.first).to_contain_text("导向轮")

def test_logged_in_fixture(logged_in_page):
    expect(logged_in_page).to_have_url("http://localhost:8000/dashboard")