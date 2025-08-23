import pytest


@pytest.fixture
def open_search_input(open_connected_shop):
    page = open_connected_shop
    search_input = page.locator("#Search-In-Inline").first
    search_input.wait_for(state="visible")
    return page, search_input