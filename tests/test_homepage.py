import pytest
import allure
from pages.header import Header
# from pages.search_page import SearchPage
 
# @pytest.mark.header
# class TestHeaderAndSearch:
#     @pytest.fixture(scope="class", autouse=True)
#     def precondition(self, open_connected_shop):
#         """Precondition: відкрити головну сторінку"""
#         self.page = open_connected_shop
#         self.header = Header(self.page)
#         yield
#         self.page.close()  
#     @allure.feature("Homepage")
#     @allure.story("Open main page and check header elements")
#     def test_open_theconnectedshop(self):
#         assert self.page.url == "https://theconnectedshop.com/"
#         assert "The Connected Shop" in self.page.title()
#     @allure.step("Перевіряємо головний логотип")
#     def test_open_theconnectedshop(self):
#         self.header.validate_logo().step
#         self.header.validate_top_links()
#         assert "The Connected Shop - Smart Locks, Smart Sensors, Smart Home & Office" in self.header.get_title()
#         self.header.assert_url("https://theconnectedshop.com/")
#         self.header.click_search_link()
 
#     @pytest.mark.search
#     def test_search_existing_product(self, open_search_input):
#         page, _ = open_search_input
#         SearchPage(page).run_test_search_existing_product()
 
#     @pytest.mark.search
#     def test_search_notexisting_product(self, open_search_input):
#         page, _ = open_search_input
#         SearchPage(page).run_test_search_notexisting_product()



#         #сторінка товару - через пошук
#         #перевірити чи додало в корзину 
#         #чи змінилася кількість товару в корзині
#         #Page object -тут теж окрема 

@allure.epic("TheConnectedShop Tests")
@allure.feature("Homepage and Search")
@allure.story("Open homepage")
@allure.severity(allure.severity_level.CRITICAL)
def test_open_theconnectedshop(open_connected_shop):
    page = open_connected_shop
    header = Header(page)
 
    with allure.step("Check homepage URL and title"):
        assert page.url == "https://theconnectedshop.com/"
        assert "The Connected Shop" in page.title()
 
    with allure.step("Validate header logo and links"):
        header.validate_logo()
        header.validate_top_links()
 
    with allure.step("Check full page title"):
        assert "The Connected Shop - Smart Locks, Smart Sensors, Smart Home & Office" in header.get_title()
 
    with allure.step("Validate homepage URL via header"):
        header.assert_url("https://theconnectedshop.com/")
 
    with allure.step("Click search link"):
        header.click_search_link()