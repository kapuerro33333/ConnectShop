import allure
from playwright.sync_api import Page, expect, TimeoutError as PWTimeout
from config.searchdata import search_text, search_text_invalid


class SearchPage:

    def __init__(self, page: Page):
        self.page = page

        # Інпут у шапці
        self.search_input = page.locator("#Search-In-Inline").first

        # Overlay
        self.overlay_container = page.locator(
            "predictive-search .predictive-search__results"
        ).first
        self.overlay_first_title = self.overlay_container.locator(
            "a.full-unstyled-link"
        ).first

        # Grid (/search)
        self.grid_product_link = page.locator(
            "a.full-unstyled-link[href*='/products/']"
        )
        self.grid_no_results_msg = page.locator("p.alert.alert--warning").first

    # ---------------- Хелпери ----------------
    @allure.step("Type query (try overlay first)")
    def _type_try_overlay(self, text: str) -> bool:
        self.search_input.wait_for(state="visible")
        self.search_input.fill("")
        self.search_input.type(text)

        try:
            self.overlay_container.wait_for(state="visible", timeout=3000)
            return self.overlay_first_title.count() > 0
        except PWTimeout:
            return False

    @allure.step("Submit query and wait grid results")
    def _submit_and_wait_grid(self, text: str) -> None:
        """Enter → очікуємо /search з товарами або 'No results'."""
        if (self.search_input.input_value() or "") != text:
            self.search_input.fill(text)
        self.search_input.press("Enter")

        self.page.wait_for_selector(
            "a.full-unstyled-link[href*='/products/'], p.alert.alert--warning",
            state="visible",
            timeout=10_000,
        )

    # ---------------- Пошук (розумний варіант) ----------------
    @allure.step("Search for valid product: {text}")
    def search_product(self, text: str | None = None) -> str:
        q = text or search_text

        # 1) пробуємо overlay без Enter
        if self._type_try_overlay(q):
            expect(self.overlay_first_title).to_be_visible(timeout=5000)
            return (self.overlay_first_title.text_content() or "").strip()

        # 2) fallback на grid (/search) з Enter
        self._submit_and_wait_grid(q)
        expect(self.grid_product_link.first).to_be_visible(timeout=5000)
        return (self.grid_product_link.first.text_content() or "").strip()

    @allure.step("Search for invalid product: {invalid_text}")
    def search_invalid_product(self, invalid_text: str | None = None) -> str:
        q = invalid_text or search_text_invalid

        try:
            self._type_try_overlay(q)
        finally:
            self._submit_and_wait_grid(q)

        expect(self.grid_no_results_msg).to_be_visible(timeout=5000)
        return (self.grid_no_results_msg.text_content() or "").strip()

    # ---------------- Простi тести ----------------
    def run_test_search_existing_product(self) -> None:
        with allure.step(f"Run simple test for EXISTING product '{search_text}'"):
            self.search_input.fill(search_text)
            self.search_input.press("Enter")
            self.page.wait_for_selector("a.full-unstyled-link[href*='/products/']", state="visible", timeout=10000)
            assert self.grid_product_link.count() > 0, "Product not found"

    def run_test_search_notexisting_product(self) -> None:
        with allure.step(f"Run simple test for NOT existing product '{search_text_invalid}'"):
            self.search_input.fill(search_text_invalid)
            self.search_input.press("Enter")
            self.page.wait_for_selector("p.alert.alert--warning", state="visible", timeout=10000)
            assert self.grid_no_results_msg.is_visible(), "No-results message is missing"