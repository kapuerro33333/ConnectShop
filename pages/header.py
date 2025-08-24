import allure
from playwright.sync_api import Page, expect


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.logo = page.locator("a.header__heading-link img.header__heading-logo")
        self._account_links = page.locator("header .header__icon--account")

    def _visible_account_link(self):
        count = self._account_links.count()
        for i in range(count):
            cand = self._account_links.nth(i)
            if cand.is_visible():
                return cand
        return self._account_links.first

    @allure.step("Validate logo in header")
    def validate_logo(self):
        expect(self.logo).to_be_visible(timeout=5000)

    @allure.step("Validate account link in header")
    def validate_account_link(self):
        link = self._visible_account_link()
        expect(link).to_be_visible(timeout=5000)
