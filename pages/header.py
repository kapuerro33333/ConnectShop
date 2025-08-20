from pages.base_page import BasePage
 
class Header(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.logo_link = page.locator('a.Header__LogoLink')
        self.primary_logo = page.locator('img.Header__LogoImage--primary')
        self.transparent_logo = page.locator('img.Header__LogoImage--transparent')
        self.account_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(0)
        self.search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(1)
        self.cart_link = page.locator('a.Heading.u-h6[href="/cart"]')
 
    def validate_logo(self):
        assert self.logo_link.is_visible(), "Logo link not found"
        assert self.logo_link.get_attribute("href") == "/", "Logo link incorrect"
        assert self.primary_logo.is_visible(), "Primary logo image not found"
        assert self.primary_logo.get_attribute("alt") == "The Connected Shop Logo"
        assert self.primary_logo.get_attribute("width") == "180"
        assert self.primary_logo.get_attribute("height") == "90.0"
        assert self.primary_logo.get_attribute("сlass") == "header__heading-logo"
 
        # assert self.transparent_logo.is_visible(), "Transparent logo image not found"
        # assert self.transparent_logo.get_attribute("alt") == "The Connected Shop Logo White"
        # assert self.transparent_logo.get_attribute("width") == "250"
        # assert self.transparent_logo.get_attribute("height") in ["75", "75px"]
 
    def validate_top_links(self):
        assert self.account_link.is_visible()
        assert self.account_link.get_attribute("href") == "/account"
 
        assert self.search_link.is_visible()
        assert self.search_link.get_attribute("href") == "/search"
        assert self.search_link.get_attribute("data-action") == "toggle-search"
 
        assert self.cart_link.is_visible()
        assert self.cart_link.get_attribute("href") == "/cart"
        assert self.cart_link.get_attribute("data-action") == "open-drawer"
        assert self.cart_link.get_attribute("data-drawer-id") == "sidebar-cart"
        assert self.cart_link.get_attribute("aria-label") == "Open cart"
    def click_search_link(self):
        self.search_link.click()