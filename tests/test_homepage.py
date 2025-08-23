import pytest
import allure
from playwright.sync_api import expect

from pages.header import Header
from pages.search_page import SearchPage
from config.searchdata import search_text as search_text_valid, search_text_invalid


@allure.feature("Homepage & Search")
class TestHeaderAndSearch:

    @pytest.mark.header
    @allure.story("Open homepage and validate header")
    @allure.severity(allure.severity_level.CRITICAL)
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
    @allure.story("Search existing product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_existing_product(self, open_search_input):
        page, _ = open_search_input
        sp = SearchPage(page)

        with allure.step(f"Search for valid product: '{search_text_valid}'"):
            first_title = sp.search_product()

        with allure.step("Validate first search result contains searched text"):
            assert search_text_valid.lower() in first_title.lower(), (
                f"Expected product title to contain '{search_text_valid}', got '{first_title}'"
            )

    @pytest.mark.search
    @allure.story("Search non-existing product")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_not_existing_product(self, open_search_input):
        page, search_input = open_search_input
        sp = SearchPage(page)

        with allure.step(f"Search for invalid product: '{search_text_invalid}'"):
            message = sp.search_invalid_product(search_text_invalid)

        with allure.step("Validate 'no results' message is displayed"):
            assert "No results found" in message, (
                f"Expected 'No results found' message, got '{message}'"
            )

    # дописати fill, existing_product,non_existing product.
    # тести виправити - локатори, падають.
    # виставити пріоритет алюре.
    # додати товар що існує, і той, що не існує - заглушка.
    # Faker скачати бібліотеку