import pytest
from playwright.sync_api import sync_playwright
from fixtures.search_fixtures import *
 
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()
 
@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def open_connected_shop(page):
    page.goto("https://theconnectedshop.com")
    return page
@pytest.fixture
def open_search_input(open_connected_shop):
    page = open_connected_shop
    
    search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(1)
    search_link.click()
   
    search_input = page.locator('input[name="q"]')
    assert search_input.is_visible(), "Search input is not visible"
    return page, search_input