def test_open_theconnectedshop(page):
    page.goto("https://theconnectedshop.com")
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
    assert  transparent_logo_image.get_attribute("alt")=="The Connected Shop Logo","Alt is not correct"
    assert  transparent_logo_image.get_attribute("width")== "250", "Width is not correct"
    assert  transparent_logo_image.get_attribute("height") in ["75", "75px"],"Height is not correct"
    # розписати Acccount, Search, Cart - розписати. 
    account_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8')
    assert account_link.is_visible(), "Account link is not visible"
    assert account_link.get_attribute("href") == "/account", "Link is not correct"
    search_link = page.locator('a.Heading.Link.Link--primary.Text--subdued.u-h8')
    assert search_link.is_visible(), "Search link is not visible"
    assert search_link.get_attribute("href") == "/search", "Link is not correct"
    assert search_link.get_attribute("data-action") == "toggle-search", "Search action is not correct"
    cart_link = page.locator('a.Heading.u-h6[href="/cart"]')
    assert cart_link.is_visible(), "Search link is not visible"
    assert cart_link.get_attribute("href") == "/cart", "Link is not correct"
    assert cart_link.get_attribute("data-action") == "open-drawer", "Cart link action is not correct"
    assert cart_link.get_attribute("data-drawer-id") == "sidebar-cart", "Cart drawer ID is incorrect"
    assert cart_link.get_attribute("aria-label") == "Open cart", "Cart aria-label is incorrect"