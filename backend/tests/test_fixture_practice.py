import os
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def equipment_count():
    return 12

def test_equipment_count(equipment_count):
    assert equipment_count == 12


@pytest.fixture
def logged_in_page(page: Page):
    # 1. 读取环境变量
    username = os.getenv("FEMCA_TEST_USERNAME")
    password = os.getenv("FEMCA_TEST_PASSWORD")

    # 2. 检查环境变量
    assert username and password, "Missing FEMCA test credentials"

    # 3. 打开登录页面
    page.goto("http://localhost:8000/login")

    # 4. 填写用户名
    page.get_by_role("textbox", name="用户名").fill(username)

    # 5. 填写密码
    page.get_by_placeholder("密码").fill(password)

    # 6. 点击登录按钮
    page.get_by_role("button", name="登录").click()

    # 7. 验证登录成功
    expect(page).to_have_url(
        "http://localhost:8000/dashboard",
        timeout=10000
    )

    # 8. 返回已经登录的 Page
    return page