import json
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Playwright
from pytest_playwright.pytest_playwright import browser

from clients.crm_client import CRMClient
from pages.auth_page import AuthPage

AUTH_FILE = "playwright/.auth/user.json"

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    value = os.getenv("BASE_URL")
    if not value:
        raise ValueError("BASE_URL is not set in .env")
    return value


@pytest.fixture(scope="session")
def access_token():
    value = os.getenv("AUTH_ACCESS_TOKEN")
    if not value:
        raise ValueError("AUTH_ACCESS_TOKEN is not set in .env")
    return value


@pytest.fixture(scope="session")
def id_token():
    value = os.getenv("AUTH_ID_TOKEN")
    if not value:
        raise ValueError("AUTH_ID_TOKEN is not set in .env")
    return value


@pytest.fixture
def crm_client(base_url, access_token, id_token):
    return CRMClient(
        base_url=base_url,
        access_token=access_token,
        id_token=id_token,
    )

# Пишем фикстуру, которая будет готовить страницу, отдавать ее тесту
# и после прохождения закрывать все сущности
# sync_playwright() не заморачиваться, просто конструкция Playwright
# внутри браузера есть контекст, внутри контекста странички
@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

@pytest.fixture(scope="session")
def auth_storage(playwright: Playwright, base_url: str):
    if os.getenv("CI"):
        return None

    if os.path.exists(AUTH_FILE):
        return AUTH_FILE

    os.makedirs("playwright/.auth", exist_ok=True)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    auth_page = AuthPage(page, base_url)
    auth_page.open()
    auth_page.select_country("Russia")
    auth_page.enter_phone_number("79104992853")
    auth_page.click_continue()

    # тут локально руками вводишь OTP
    auth_page.wait_until_logged_in()

    context.storage_state(path=AUTH_FILE)
    context.close()
    browser.close()

    return AUTH_FILE


@pytest.fixture
def authorized_page(playwright: Playwright, base_url: str, auth_storage):
    browser = playwright.chromium.launch(headless=True)

    access_token = os.getenv("AUTH_ACCESS_TOKEN")
    id_token = os.getenv("AUTH_ID_TOKEN")

    if os.getenv("CI") and access_token and id_token:
        context = browser.new_context()
        auth_data = {
            "AccessToken": access_token,
            "IdToken": id_token,
        }
        auth_json = json.dumps(auth_data)
        auth_json_js_literal = json.dumps(auth_json)

        context.add_init_script(
            f"""
            window.localStorage.setItem('auth', {auth_json_js_literal});
            """
        )
    else:
        context = browser.new_context(storage_state=auth_storage)

    page = context.new_page()
    yield page
    context.close()
    browser.close()