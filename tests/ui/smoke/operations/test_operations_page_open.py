import json
import os
import pytest
from playwright.sync_api import sync_playwright


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
