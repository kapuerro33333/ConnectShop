class BasePage:
    def __init__(self, page):
        self.page = page
    def get_title(self):
        return self.page.title()
    
    def assert_url(self, expected_url: str):
        actual_url = self.page.url
        assert actual_url == expected_url, f"Очікувався URL: {expected_url}, але був: {actual_url}"
 