from pages.base_page import BasePage

class SearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator('input[name="q"]')
        self.results = page.locator('.Search__Results .ProductItem__Title')
        self.no_results_message = page.locator('.Search__NoResults')

    def search_product(self, text):
        self.search_input.fill(text)
        self.search_input.press("Enter")
        return [r.inner_text().lower() for r in self.results.all()]

    def search_invalid_product(self, text):
        self.search_input.fill(text)
        self.search_input.press("Enter")
        message = self.no_results_message.inner_text()
        return message, self.search_input.input_value()