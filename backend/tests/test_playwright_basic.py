import re
from playwright.sync_api import Page, expect
from pathlib import Path

def test_page_title(page: Page):
    # Step 1: Open the test website
    page.goto("https://example.com")

    # Step 2: Verify the page title
    expect(page).to_have_title("Example Domain")

def test_python_website_title(page: Page):
    page.goto("https://www.python.org/")

    expect(page).to_have_title(re.compile("Python"))

def test_register_form(page: Page):
    html_file = Path("practice_pages/register.html").resolve()
    page.goto(html_file.as_uri())

    page.get_by_role("textbox", name="Username").fill("alice123")
    page.get_by_role("textbox", name="Email").fill("alice@example.com")

    expect(page.get_by_role("textbox", name="Username")).to_have_value("alice123")
    expect(page.get_by_role("textbox", name="Email")).to_have_value("alice@example.com")

    page.get_by_role("button", name="Register").click()

    expect(
        page.get_by_text("Registration successful!")
    ).to_be_visible()

def test_success_message_hidden_before_submit(page: Page):
    html_file = Path("practice_pages/register.html").resolve()
    page.goto(html_file.as_uri())

    expect(page.get_by_text("Registration successful!")).to_be_hidden()

def test_register_invalid_email(page: Page):
    html_file = Path("practice_pages/register.html").resolve()
    page.goto(html_file.as_uri())

    page.get_by_role("textbox", name="Username").fill("alice123")
    page.get_by_role("textbox", name="Email").fill("alice123")
    page.get_by_role("button", name="Register").click()

    expect(page.get_by_text("Registration successful!")).to_be_hidden()
    expect(page.locator("#email:invalid")).to_have_count(1)

def test_register_input_count(page: Page):
    html_file = Path("practice_pages/register.html").resolve()
    page.goto(html_file.as_uri())

    expect(page.locator("input")).to_have_count(2)