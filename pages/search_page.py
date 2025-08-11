from config.searchdata import search_text, search_text_invalid
from pages.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.search_input = page.locator('input[name="q"]')
        self.results_links = page.locator('h2.ProductItem__Title a')
        self.no_results_msg = page.locator('div.Segment__Content p')

    def search_product(self, text: str):
        self.search_input.fill(text)
        self.search_input.press("Enter")
        self.page.wait_for_selector(
            'h2.ProductItem__Title a, div.Segment__Content p',
            state='visible',
            timeout=10000
        )
        return [t.strip().lower() for t in self.results_links.all_text_contents()]

    def search_invalid_product(self, text: str):
        self.search_input.fill(text)
        self.search_input.press("Enter")
        self.page.wait_for_selector('div.Segment__Content p', state='visible', timeout=10000)
        message = (self.no_results_msg.first.text_content() or "").strip()
        return message, self.search_input.input_value()


    def run_test_search_existing_product(self):
        results = self.search_product(search_text)
        assert any(search_text.lower() in r for r in results), \
            f"'{search_text}' not found in search results: {results}"

    def run_test_search_notexisting_product(self):
        message_text, input_value = self.search_invalid_product(search_text_invalid)
        assert input_value == search_text_invalid, "Incorrect input value"
        assert "No results" in message_text, f"Unexpected message: {message_text}"