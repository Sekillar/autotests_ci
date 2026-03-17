from pages.base_page import BasePage

class OperationsPage(BasePage):
    def open(self):
        self.goto("/operations")
        self.page.wait_for_load_state("domcontentloaded")

    def total_balance(self):
        return self.page.get_by_text("Total balance", exact=True)

    def total_balance_value(self):
        return self.page.locator("div[class*='balanceValue']").filter(has_text="pts")

    def operations_table(self):
        return self.page.get_by_text("Transactions", exact=True)

    def transactions_rows(self):
        return self.page.locator("div[class*='row']")

    def export_button(self):
        return self.page.get_by_role("button", name="Export")

    def pagination(self):
        return self.page.locator("div[class*='pagination_center']")
