import allure
from playwright.sync_api import Page, expect
from config.searchdata import search_text as search_text_valid


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        # Поле пошуку в хедері (inline)
        self.search_input = page.locator("#Search-In-Inline")
        # Беремо лише перший заголовок товару, щоб уникнути strict-mode
        self.product_title = page.locator(
            "a.full-unstyled-link .card__heading__product-title"
        ).first
        # Точне повідомлення Shopify-теми при відсутності результатів
        self.no_results_message = page.locator("p.alert.alert--warning")

    @allure.step("Search for valid product")
    def search_product(self) -> str:
        """Шукає валідний товар (з config.searchdata.search_text) та повертає назву першого результату."""
        self.search_input.fill(search_text_valid)
        self.search_input.press("Enter")
        expect(self.product_title).to_be_visible(timeout=5000)
        return self.product_title.inner_text().strip()

    @allure.step("Search for invalid product: {invalid_text}")
    def search_invalid_product(self, invalid_text: str) -> str:
        """Шукає неіснуючий товар і повертає текст повідомлення 'No results found ...'."""
        self.search_input.fill(invalid_text)
        self.search_input.press("Enter")
        expect(self.no_results_message).to_be_visible(timeout=5000)
        return self.no_results_message.inner_text().strip()