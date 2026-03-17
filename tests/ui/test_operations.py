import json
import os
from time import sleep

import pytest
from playwright.sync_api import sync_playwright, expect
from dotenv import load_dotenv

from pages.operations_page import OperationsPage

load_dotenv()


@pytest.mark.smoke
@pytest.mark.ui
def test_operations_page_returns_200():

    base_url = os.getenv("BASE_URL")
    access_token = os.getenv("AUTH_ACCESS_TOKEN")
    id_token = os.getenv("AUTH_ID_TOKEN")

    assert base_url, "BASE_URL is not set"
    assert access_token, "AUTH_ACCESS_TOKEN is not set"
    assert id_token, "AUTH_ID_TOKEN is not set"

    operations_url = f"{base_url}/operations"

    auth = {
        "AccessToken": access_token,
        "IdToken": id_token,
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # кладём auth в localStorage
        auth_json = json.dumps(auth)
        auth_json_js_literal = json.dumps(auth_json)

        context.add_init_script(
            f"""
            localStorage.setItem("auth", {auth_json_js_literal});
            """
        )

        page = context.new_page()

        # открываем страницу
        response = page.goto(operations_url, wait_until="domcontentloaded")

        # проверяем код ответа
        assert response is not None, "No response received"
        assert response.status == 200, f"Expected 200 but got {response.status}"

        # проверяем что реально попали на страницу операций
        assert "/operations" in page.url

        browser.close()

@pytest.mark.smoke
@pytest.mark.ui
def test_operations_page_opens_auth_user(authorized_page, base_url):
    authorized_page.goto(base_url + "/operations")

@pytest.mark.smoke
@pytest.mark.ui
def test_total_balance_label_visible(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    locator = operations_page.total_balance()
    expect(locator).to_be_visible()

@pytest.mark.smoke
@pytest.mark.ui
def test_total_balance_card_visible_not_empty(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    locator = operations_page.total_balance()
    expect(locator).to_be_visible()

@pytest.mark.smoke
@pytest.mark.ui
def test_total_balance_not_zero(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    value_locator = operations_page.total_balance_value()
    expect(value_locator).to_be_visible()

    text = value_locator.inner_text()
    # "31,173.08 pts"

    # вытаскиваем число
    number = float(
        text.replace("pts", "")
            .replace(",", "")
            .strip()
    )

    assert number != 0, f"Balance is zero: {text}"

@pytest.mark.smoke
@pytest.mark.ui
def test_transactions_header_is_visible(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    locator = operations_page.operations_table()
    expect(locator).to_be_visible()

@pytest.mark.smoke
@pytest.mark.ui
def test_transactions_table_not_empty(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    rows = operations_page.transactions_rows()
    expect(rows.first).to_be_visible()
    assert rows.count() > 0, "Transactions table is empty"

@pytest.mark.smoke
@pytest.mark.ui
def test_export_button_is_visible(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()

    locator = operations_page.export_button()
    expect(locator).to_be_visible()

@pytest.mark.smoke
@pytest.mark.ui
def test_pagination_is_visible(authorized_page, base_url):
    operations_page = OperationsPage(authorized_page, base_url)
    operations_page.open()
    operations_page.page.wait_for_load_state("networkidle")
    locator = operations_page.pagination()
    expect(locator).to_be_visible()