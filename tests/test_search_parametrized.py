import pytest
import allure

from config.searchdata import (
    SEARCH_VALUES_EXISTING,
    SEARCH_VALUES_NON_EXISTING,
    get_random_existing,
    get_random_non_existing,
)
from pages.product_page import ProductPage


@allure.epic("Connected Shop Tests")
@allure.feature("Search (Parametrized)")
class TestSearchParametrized:

    @pytest.mark.search
    @pytest.mark.parametrize("search_value", SEARCH_VALUES_EXISTING)
    @allure.story("Search existing products")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_all_existing_products(self, open_search_input, search_value):
        page, _ = open_search_input

        with allure.step(f"Search for existing product: '{search_value}'"):
            page.locator("#Search-In-Inline").fill(search_value)
            page.locator("#Search-In-Inline").press("Enter")

        with allure.step("Validate results are found"):
            page.wait_for_selector(
                "a.full-unstyled-link[href*='/products/']",
                state="visible",
                timeout=10000,
            )
            assert (
                page.locator("a.full-unstyled-link[href*='/products/']").count() > 0
            ), f"Expected results for '{search_value}', but none found"

    @pytest.mark.search
    @pytest.mark.parametrize("search_value", SEARCH_VALUES_NON_EXISTING)
    @allure.story("Search non-existing products")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_all_non_existing_products(self, open_search_input, search_value):
        page, _ = open_search_input

        with allure.step(f"Search for non-existing product: '{search_value}'"):
            page.locator("#Search-In-Inline").fill(search_value)
            page.locator("#Search-In-Inline").press("Enter")

        with allure.step("Validate no-results message"):
            page.wait_for_selector(
                "p.alert.alert--warning, a.full-unstyled-link[href*='/products/']",
                state="visible",
                timeout=10000,
            )
            assert page.locator("p.alert.alert--warning").is_visible(), (
                f"Expected 'No results' message for '{search_value}', but not found"
            )


@allure.epic("Connected Shop Tests")
@allure.feature("Search (Optional)")
class TestSearchRandomOptional:

    @pytest.mark.search
    @pytest.mark.optional
    @allure.story("Random existing product")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_random_existing(self, open_search_input):
        page, _ = open_search_input
        q = get_random_existing()

        with allure.step(f"Search for random existing product: '{q}'"):
            page.locator("#Search-In-Inline").fill(q)
            page.locator("#Search-In-Inline").press("Enter")

        with allure.step("Validate results"):
            page.wait_for_selector(
                "a.full-unstyled-link[href*='/products/']",
                state="visible",
                timeout=10000,
            )
            found = page.locator("a.full-unstyled-link[href*='/products/']").count() > 0
            allure.attach(
                body=f"Found results: {found} for query '{q}'",
                name="Random existing search info",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert found, f"No products found for supposed existing query '{q}'"

    @pytest.mark.search
    @pytest.mark.optional
    @allure.story("Random non-existing product")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_search_random_non_existing(self, open_search_input):
        page, _ = open_search_input
        q = get_random_non_existing()

        with allure.step(f"Search for random non-existing product: '{q}'"):
            page.locator("#Search-In-Inline").fill(q)
            page.locator("#Search-In-Inline").press("Enter")

        with allure.step("Validate no-results message or attach context"):
            page.wait_for_selector(
                "p.alert.alert--warning, a.full-unstyled-link[href*='/products/']",
                state="visible",
                timeout=10000,
            )
            has_no_results = page.locator("p.alert.alert--warning").is_visible()
            if not has_no_results:
                cnt = page.locator("a.full-unstyled-link[href*='/products/']").count()
                allure.attach(
                    body=f"Unexpected results ({cnt}) for query '{q}'",
                    name="Random non-existing search info",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert has_no_results, f"'No results' message not visible for '{q}'"