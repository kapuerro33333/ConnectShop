import pytest



@pytest.fixture
def open_search_input(open_connected_shop):
    page = open_connected_shop
    search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(1)
    search_link.click()
    search_input = page.locator('input[name="q"]')
    assert search_input.is_visible(), "Search input is not visible"
    return page, search_input