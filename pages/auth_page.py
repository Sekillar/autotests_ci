from playwright.sync_api import expect

from pages.base_page import BasePage

class AuthPage(BasePage):
    def open(self):
        self.goto("/authorization")
# Проверяем, что страница открылась и видна через встроенный метод пейджи
        self.page.wait_for_load_state("domcontentloaded")

    def select_country(self, country:str):
        country_field = (
            self.page.locator("label")
            .filter(has_text="Country")
            .locator('div[aria-haspopup="listbox"]')
        )
        country_field.click()
        self.page.get_by_role("menuitem", name=country).click()

    def enter_phone_number(self, phone_number: str):
        phone_field = (
            self.page.locator("label")
            .filter(has_text="Phone")
            .locator('input[type="tel"]')
        )
        phone_field.fill(phone_number)

    def click_continue(self):
        button = self.page.get_by_role("button", name="Continue")
        expect(button).to_be_enabled()
        button.click()

    def wait_until_logged_in(self):
        self.page.wait_for_url("**/operations", timeout=120_000)

    def login_with_phone(self, country: str, phone: str):
        self.select_country(country)
        self.enter_phone_number(phone)
        self.click_continue()
        self.wait_until_logged_in()

