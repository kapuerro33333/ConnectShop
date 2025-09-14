import pytest
import allure
from faker import Faker

from pages.header import Header
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from config.searchdata import search_text, search_text_invalid, get_random_search_value

faker = Faker()


@allure.epic("Connected Shop Tests")
@allure.feature("Homepage & Header")
class TestHeaderAndSearch:

    @pytest.mark.header
    @pytest.mark.smoke
    @allure.story("Open homepage and validate header")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_open_homepage_and_header(self, open_connected_shop):
        page = open_connected_shop
        header = Header(page)

        with allure.step("Check homepage URL and title"):
            assert page.url.startswith("https://theconnectedshop.com")
            assert "The Connected Shop" in page.title()

        with allure.step("Validate logo in header"):
            header.validate_logo()

        with allure.step("Validate account link in header"):
            header.validate_account_link()

    @pytest.mark.search
    @pytest.mark.smoke
    @allure.story("Search existing product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_existing_product(self, open_search_input):
        page, _ = open_search_input
        with allure.step(f"Search for valid product: {search_text}"):
            SearchPage(page).run_test_search_existing_product()

    @pytest.mark.search
    @allure.story("Search non-existing product")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_not_existing_product(self, open_search_input):
        page, _ = open_search_input
        with allure.step(f"Search for invalid product: {search_text_invalid}"):
            SearchPage(page).run_test_search_notexisting_product()


@allure.epic("Connected Shop Tests")
@allure.feature("Cart")
class TestCartFlow:

    @pytest.mark.smoke
    @allure.story("Add existing product to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_existing_product_to_cart(self, open_search_input):
        page, _ = open_search_input

        with allure.step(f"Search and open search results for: {search_text}"):
            sp = SearchPage(page)
            sp.run_test_search_existing_product()

            # гарантуємо /search
            if "/search" not in page.url:
                view_all = page.locator(
                    "a.search__view-all, a:has-text('View all results'):visible"
                ).first
                if view_all.count() > 0 and view_all.is_visible():
                    view_all.click()
                else:
                    page.locator("#Search-In-Inline").first.press("Enter")

            page.wait_for_selector(
                "a.full-unstyled-link[href*='/products/']",
                state="visible",
                timeout=10000,
            )

        with allure.step("Click 'Add to cart' and validate cart"):
            ProductPage(page).add_to_cart()


@allure.epic("Connected Shop Tests")
@allure.feature("Search (Optional)")
class TestRandomSearch:

    @pytest.mark.search
    @pytest.mark.optional
    @allure.story("Search random product from predefined list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_random_product(self, open_search_input):
        page, _ = open_search_input
        q = get_random_search_value()

        with allure.step(f"Search for random product: '{q}'"):
            page.locator("#Search-In-Inline").fill(q)
            page.locator("#Search-In-Inline").press("Enter")
            page.wait_for_selector(
                "a.full-unstyled-link[href*='/products/'], p.alert.alert--warning",
                state="visible",
                timeout=10000,
            )

        with allure.step("Attach screenshot of search results"):
            allure.attach(
                page.screenshot(),
                name=f"Search_{q}",
                attachment_type=allure.attachment_type.PNG,
            )

        with allure.step("Validate results or no-results message"):
            has_products = page.locator("a.full-unstyled-link[href*='/products/']").count() > 0
            has_no_results = page.locator("p.alert.alert--warning").is_visible()

            if has_products:
                allure.attach(
                    body=f"Results found for: {q}",
                    name="Search result info",
                    attachment_type=allure.attachment_type.TEXT,
                )
            elif has_no_results:
                allure.attach(
                    body=f"No results found for: {q}",
                    name="Search result info",
                    attachment_type=allure.attachment_type.TEXT,
                )
            else:
                pytest.fail(f"No products and no 'No results' message for query '{q}'")
    # виставити пріоритет алюре.
    # Faker скачати бібліотеку
    # негативні кейси: негативне значення, забрати товар з корзини.  
    # окремо розписати Add to cart 
    # API повторити
    
    
# import random
# SEARCH_VALUES = [
#     "smart door lock",
#     "wifi camera",
#     "robot vacuum",
#     "doorbell",
#     "bluetooth speaker",
#     "gaming headset",
#     "wireless charger",
#     "laptop stand",
#     "mechanical keyboard",
#     "usb hub"
# ]
# def get_random_search_value() -> str:
#     return random.choice(SEARCH_VALUES)
 