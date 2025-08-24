import pytest
import allure
from pages.header import Header
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from config.searchdata import search_text, search_text_invalid
from faker import Faker


faker = Faker()

@allure.epic("Critical tests")
@allure.feature("Homepage & Search")
class TestHeaderAndSearch:

    @pytest.mark.header
    @pytest.mark.smoke
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


# --- Додатковий smoke: add to cart (опційно, якщо вже додали ProductPage) ---


@allure.epic("Cart tests")
@allure.feature("Cart")
class TestCartFlow:

    @pytest.mark.smoke
    @allure.story("Add existing product to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_existing_product_to_cart(self, open_search_input):
        page, _ = open_search_input

        with allure.step(f"Search and open search results for: {search_text}"):
            sp = SearchPage(page)
            # Пошук (оверлей або грід) — лише перевірка, що результат є
            sp.run_test_search_existing_product()

            # Гарантовано потрапляємо на сторінку з грідом /search:
            if "/search" not in page.url:
                view_all = page.locator("a.search__view-all, a:has-text('View all results')").first
                if view_all.count() > 0 and view_all.is_visible():
                    view_all.click()
                else:
                    # fallback: просто Enter у хедерному інпуті
                    page.locator("#Search-In-Inline").first.press("Enter")

            # чекаємо, поки у гріді будуть посилання на продукти
            page.wait_for_selector("a.full-unstyled-link[href*='/products/']", state="visible", timeout=10000)

        with allure.step("Click 'Add to cart' and validate cart"):
            ProductPage(page).add_to_cart()
    # дописати fill, existing_product,non_existing product.
    # тести виправити - локатори, падають.
    # виставити пріоритет алюре.
    # додати товар що існує, і той, що не існує - заглушка.
    # Faker скачати бібліотеку