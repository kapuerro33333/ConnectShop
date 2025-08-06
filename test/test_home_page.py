from config.searchdata import search_text
from config.searchdata import search_text_invalid
 
def test_open_theconnectedshop(open_connected_shop):
    #page.goto("https://theconnectedshop.com")
    page = open_connected_shop
    assert page.url == "https://theconnectedshop.com/", f"URL неправильний: {page.url}"
    title = page.title()
    assert "The Connected Shop" in title, f"Title неправильний: {title}"
    logo_link = page.locator ('a.Header__LogoLink')
    assert logo_link.is_visible(),"Link is not found"
    assert logo_link.get_attribute("href")=="/","Link is not correct"
    primary_logo_image = page.locator('img.Header__LogoImage--primary')
    assert  primary_logo_image.is_visible(),"Img is not found"
    assert  primary_logo_image.get_attribute("alt")=="The Connected Shop Logo","Alt is not correct"
    assert  primary_logo_image.get_attribute("width")== "250", "Width is not correct"
    assert  primary_logo_image.get_attribute("height")in ["75", "75px"],"Height is not correct"
     #дописати атрибути
    transparent_logo_image = page.locator('img.Header__LogoImage--transparent')
    assert  transparent_logo_image.is_visible(),"Img is not found"
    assert  transparent_logo_image.get_attribute("alt")=="The Connected Shop Logo White","Alt is not correct"
    assert  transparent_logo_image.get_attribute("width")== "250", "Width is not correct"
    assert  transparent_logo_image.get_attribute("height") in ["75", "75px"],"Height is not correct"
    # розписати Acccount, Search, Cart - розписати. 
    account_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(0)
    assert account_link.is_visible(), "Account link is not visible"
    assert account_link.get_attribute("href") == "/account", "Link is not correct"
    search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(1)
    assert search_link.is_visible(), "Search link is not visible"
    assert search_link.get_attribute("href") == "/search", "Link is not correct"
    assert search_link.get_attribute("data-action") == "toggle-search", "Search action is not correct"
    cart_link = page.locator('a.Heading.u-h6[href="/cart"]')
    assert cart_link.is_visible(), "Cart link is not visible"
    assert cart_link.get_attribute("href") == "/cart", "Link is not correct"
    assert cart_link.get_attribute("data-action") == "open-drawer", "Cart link action is not correct"
    assert cart_link.get_attribute("data-drawer-id") == "sidebar-cart", "Cart drawer ID is incorrect"
    assert cart_link.get_attribute("aria-label") == "Open cart", "Cart aria-label is incorrect"

def test_search_existing_product(open_search_input):
    page, search_input = open_search_input
    #page.goto("https://theconnectedshop.com")
    #search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8').nth(1)
    #search_link.click()
    #search_input = page.locator ('input[name="q"]')
    #assert search_input.get_attribute("name") =="q","Input name is not correct"
    #assert search_input.get_attribute("autocomplete") =="off","Autocomplete name is not correct"
    # assert search_input.get_attribute("autocapitalize") =="off","Autocapitalize name is not correct"
    # assert search_input.get_attribute("aria-label") =="Search...","Area-label name is not correct"
    # assert search_input.get_attribute("placeholder") =="Search...","Placeholder name is not correct"
    #search_text = "Bluetooth Drawer Lock"
    search_input.fill(search_text)
    page.wait_for_selector('h2.ProductItem__Title a', state="visible")

    # Збираємо всі результати
    results = [r.strip().lower() for r in page.locator('h2.ProductItem__Title a').all_text_contents()]
    print(results) 

    # Перевіряємо, що наш товар є серед результатів
    assert any(search_text.lower() in r for r in results), \
        f"'{search_text}' not found in search results: {results}"
def test_search_notexisting_product(open_search_input):
    page, search_input = open_search_input
    search_input.fill(search_text_invalid)
    search_input.press("Enter")
    page.wait_for_selector('div.Segment__Content p')
    input_value = search_input.input_value()
    assert input_value == search_text_invalid, f"Очікувалось '{search_text_invalid}', але отримано '{input_value}'"
    search_output_2 = page.locator('div.Segment__Content p').first
    assert search_output_2.is_visible(), "No-results message is not displayed"
    assert search_output_2.text_content().strip() == "No results could be found", "Displayed message text is incorrect"
    # виправити 2 останніх. 
    #- налаштувати проект для нового проекту
    #- 
