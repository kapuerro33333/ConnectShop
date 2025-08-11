from pages.header import Header
from pages.search_page import SearchPage

def test_open_theconnectedshop(open_connected_shop):
    page = open_connected_shop
    header = Header(page)

    assert page.url == "https://theconnectedshop.com/"
    assert "The Connected Shop" in page.title()
    header.validate_logo()
    header.validate_top_links()
    assert "The Connected Shop - Smart Locks, Smart Sensors, Smart Home & Office" in header.get_title()
    header.assert_url("https://theconnectedshop.com/")
    header.click_search_link()

def test_search_existing_product(open_search_input):
    page, _ = open_search_input
    SearchPage(page).run_test_search_existing_product()

def test_search_notexisting_product(open_search_input):
    page, _ = open_search_input
    SearchPage(page).run_test_search_notexisting_product()
