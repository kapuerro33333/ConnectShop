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

@pytest.fixture(scope="class")

def open_connected_shop(browser):

    page = browser.new_page()

    page.goto("https://theconnectedshop.com/")

    yield page

    page.close()

 

# @pytest.fixture
# def open_connected_shop(page):
#     page.goto("https://theconnectedshop.com")
#     return page

import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    # Зафіксуємо десктопний viewport, щоб видимою була саме desktop-іконка акаунта
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "geolocation": None,
        "permissions": [],
    }
    