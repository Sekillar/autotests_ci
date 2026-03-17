from time import sleep

import pytest

from pages.base_page import BasePage
from pages.auth_page import AuthPage

# Локальный тест, убрать из пайплайна
@pytest.mark.local_only
def test_login_with_phone(page, base_url):
    home_page = AuthPage(page, base_url)
    home_page.goto()
    home_page.login_with_phone("Russia", "79104992853")
    sleep(5)




